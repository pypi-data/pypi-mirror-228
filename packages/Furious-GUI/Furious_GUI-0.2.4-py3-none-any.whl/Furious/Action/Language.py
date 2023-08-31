from Furious.Gui.Action import Action
from Furious.Widget.Widget import Menu
from Furious.Utility.Constants import APP
from Furious.Utility.Utility import bootstrapIcon
from Furious.Utility.Translator import (
    Translatable,
    gettext as _,
    ABBR_TO_LANGUAGE,
    LANGUAGE_TO_ABBR,
)

import logging

logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGE = tuple(LANGUAGE_TO_ABBR.values())


class LanguageChildAction(Action):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def triggeredCallback(self, checked):
        checkedLanguage = LANGUAGE_TO_ABBR[self.text()]

        if APP().Language != checkedLanguage:
            logger.info(f'set language to \'{self.text()}\'')

            APP().Language = checkedLanguage

            Translatable.retranslateAll()


class LanguageAction(Action):
    def __init__(self):
        super().__init__(
            _('Language'),
            icon=bootstrapIcon('globe2.svg'),
            menu=Menu(
                *list(
                    LanguageChildAction(
                        # Language representation
                        text,
                        checkable=True,
                        checked=text == ABBR_TO_LANGUAGE[APP().Language],
                    )
                    for text in list(LANGUAGE_TO_ABBR.keys())
                ),
            ),
        )
