"""Top-level package for morphinder."""
import logging


log = logging.getLogger(__name__)

__author__ = "Florian Matter"
__email__ = "fmatter@mailbox.org"
__version__ = "0.0.2"


def identify_complex_stem_position(obj, stem):
    indices = []
    objs = obj.split("-")
    stems = stem.split("-")
    for st in stems:
        if st in objs:
            indices.append(objs.index(st))
    return indices


class Morphinder:
    def __init__(self, lexicon, complain=True):
        self.cache = {}
        self.failed_cache = set()
        self.lexicon = lexicon
        self.complain = complain

    def return_values(self, obj, gloss, morph_id, sense):
        self.cache[(obj, gloss)] = (morph_id, sense)
        return (morph_id, sense)

    def retrieve_morph_id(
        self,
        obj,
        gloss,
        morph_type,
        sense_key=None,
        id_key="ID",
        type_key="Type",
        gloss_key="Gloss",
        form_key="Form",
    ):  # pylint: disable=too-many-arguments
        if (obj, gloss) in self.cache:
            return self.cache[(obj, gloss)]
        if (
            obj,
            gloss,
        ) in self.failed_cache:  # failing silently (except for the first try)
            return None, None
        bare_gloss = gloss.strip("=").strip("-")
        candidates = self.lexicon[
            (self.lexicon[form_key].apply(lambda x: obj == x))
            & (self.lexicon[gloss_key].apply(lambda x: bare_gloss in x))
        ]
        if len(candidates) == 1:
            if sense_key:
                morph_id, sense = (
                    candidates.iloc[0][id_key],
                    candidates.iloc[0][sense_key][
                        candidates.iloc[0][gloss_key].index(bare_gloss)
                    ],
                )
                return self.return_values(obj, gloss, morph_id, sense)
            return self.return_values(obj, gloss, candidates.iloc[0][id_key], None)
        if len(candidates) > 0:
            if type_key in candidates:
                narrow_candidates = candidates[candidates[type_key] == morph_type]
                if len(narrow_candidates) == 1:
                    if sense_key:
                        return self.return_values(
                            obj,
                            gloss,
                            narrow_candidates.iloc[0][id_key],
                            narrow_candidates.iloc[0][sense_key][
                                narrow_candidates.iloc[0][gloss_key].index(bare_gloss)
                            ],
                        )
                    return narrow_candidates.iloc[0][id_key]
            if self.complain:
                log.warning(
                    f"Multiple lexicon entries for {obj} '{gloss}', using the first hit:"
                )
                print(morph_type)
                print(candidates)
            if sense_key:
                return self.return_values(
                    obj,
                    gloss,
                    candidates.iloc[0][id_key],
                    candidates.iloc[0][sense_key][
                        candidates.iloc[0][gloss_key].index(bare_gloss)
                    ],
                )
            return self.return_values(obj, gloss, candidates.iloc[0][id_key], None)
        if self.complain:
            log.warning(f"No hits for /{obj}/ '{gloss}' in lexicon!")
        self.failed_cache.add((obj, gloss))
        return None, None
