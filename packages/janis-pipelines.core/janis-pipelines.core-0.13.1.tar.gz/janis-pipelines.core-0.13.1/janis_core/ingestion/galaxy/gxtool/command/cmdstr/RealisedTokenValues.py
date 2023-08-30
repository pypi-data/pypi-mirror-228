

from __future__ import annotations
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from janis_core.ingestion.galaxy.gxtool.model import XMLTool

from ..tokens import Token
from ..tokens import tokenize
from . import constructs
from . import utils
from .analysis import is_bool_select


class RealisedTokens:
    """
    class exists to expose hidden values within galaxy params
    each galaxy select param can hold any number of text values,
    and each text value may have 1 or more words / keyval pairs
    """
    def __init__(self, values: list[list[Token]], original: Token):
        self.tlists = values
        self.original = original
        self.transfer_attributes()

    def transfer_attributes(self) -> None:
        for tlist in self.tlists:
            for token in tlist:
                token.gxparam = self.original.gxparam
                token.construct = self.original.construct
                token.in_conditional = self.original.in_conditional
                token.in_loop = self.original.in_loop
        
    def get_original_token(self) -> Token:
        return self.original
    
    def get_default_token(self) -> Token:
        for tlist in self.tlists:
            if len(tlist) > 0:
                return tlist[0]
        return self.get_original_token()
    
    def get_first_word(self) -> str:
        return self.get_default_token().text
    
    def __repr__(self) -> str:
        strvalues: list[str] = []
        for tlist in self.tlists:
            strvalues.append(' '.join([token.text for token in tlist]))
        return f'RealisedTokenValues: {", ".join(strvalues)}'


class RealisedTokenFactory:
    def __init__(self, xmltool: Optional[XMLTool]):
        self.xmltool = xmltool
        self.tracker = constructs.ConstructTracker()  # this is all a bit ugly

    def try_tokenise_text(self, text: str) -> list[RealisedTokens]:
        rtvs: list[RealisedTokens] = []
        line_num = 0
        for line in utils.split_lines(text):
            self.tracker.update(line)
            if self.should_tokenise_line(line):
                rtvs += self.try_tokenise_line(line, line_num)
            line_num += 1
        return rtvs

    def should_tokenise_line(self, line: str) -> bool:
        if self.tracker.active_is_boundary(line) or self.tracker.within_banned_segment:
            return False
        return True
    
    def try_tokenise_line(self, line: str, line_num: Optional[int]=None) -> list[RealisedTokens]:
        try:
            line_tokens = self.create_line_tokens(line)
            line_tokens = self.set_token_context(line_tokens, line_num)
            return self.create_realised_values(line_tokens)
        except ValueError:
            return []

    def create_line_tokens(self, line: str) -> list[Token]:
        line_tokens: list[Token] = []
        for word in utils.split_to_words(line):
            line_tokens += tokenize(word, xmltool=self.xmltool)
        return line_tokens

    def set_token_context(self, line_tokens: list[Token], line_num: Optional[int]=None) -> list[Token]:
        for token in line_tokens:
            if line_num is not None:
                token.line = line_num
            token.construct = self.tracker.stack.current_construct
            token.in_conditional = self.tracker.within_conditional
            token.in_loop = self.tracker.within_loop
        return line_tokens

    def create_realised_values(self, line_tokens: list[Token]) -> list[RealisedTokens]:
        out: list[RealisedTokens] = []
        for token in line_tokens:
            if is_bool_select(token):
                vals_as_text: list[str] = token.gxparam.non_null_values #type: ignore
                vals_as_tlists = [self.create_line_tokens(text) for text in vals_as_text]
                out.append(RealisedTokens(values=vals_as_tlists, original=token))
            else:
                out.append(RealisedTokens(values=[[token]], original=token))
        return out



