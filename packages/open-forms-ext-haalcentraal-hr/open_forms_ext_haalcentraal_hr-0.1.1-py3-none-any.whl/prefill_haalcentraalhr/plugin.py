import logging

from django.utils.translation import gettext_lazy as _

from glom import GlomError, glom
from openforms.authentication.constants import AuthAttribute
from openforms.plugins.exceptions import InvalidPluginConfiguration
from openforms.prefill.base import BasePlugin
from openforms.prefill.constants import IdentifierRoles
from openforms.prefill.registry import register
from openforms.submissions.models import Submission
from openforms.typing import JSONObject
from zds_client import ClientError

from .constants import Attributes
from .models import HaalCentraalHRConfig

logger = logging.getLogger(__name__)


class HaalCentraalHRZGWClientError(Exception):
    pass


@register("haalcentraal_hr")
class HaalCentraalHRPrefill(BasePlugin):
    verbose_name = _("Haal Centraal HR")
    requires_auth = AuthAttribute.kvk

    def get_available_attributes(self) -> list[tuple[str, str]]:
        return Attributes.choices

    def get_identifier_value(
        self, submission: Submission, identifier_role: str
    ) -> str | None:
        if not submission.is_authenticated:
            return

        if (
            identifier_role == IdentifierRoles.main
            and submission.auth_info.attribute == self.requires_auth
        ):
            return submission.auth_info.value

    def extract_requested_attributes(
        self, attributes: list[str], data: JSONObject | None
    ) -> JSONObject:
        if not data:
            return {}

        values = dict()
        for attr in attributes:
            try:
                values[attr] = glom(data, attr)
            except GlomError as exc:
                logger.warning(
                    "Missing expected attribute '%s' in Haal Centraal HR response",
                    attr,
                    exc_info=exc,
                )

        return values

    def get_prefill_values(
        self,
        submission: Submission,
        attributes: list[str],
        identifier_role: str = IdentifierRoles.main,
    ) -> JSONObject:
        # check if submission was logged in with the identifier we're interested
        if not (kvk_value := self.get_identifier_value(submission, identifier_role)):
            return {}

        config = HaalCentraalHRConfig.get_solo()

        haal_centraal_hr_client = config.build_client(submission=submission)
        if haal_centraal_hr_client is None:
            logger.exception("Haal Centraal HR service not configured.")
            return {}

        try:
            data = haal_centraal_hr_client.retrieve(
                "RaadpleegMaatschappelijkeActiviteitOpKvKnummer",
                url=f"maatschappelijkeactiviteiten/{kvk_value}",
                request_kwargs={
                    "headers": {
                        "Accept": "application/hal+json",
                    },
                },
            )
        except HaalCentraalHRZGWClientError as e:
            logger.exception(
                "Exception while making request to Haal Centraal HR", exc_info=e
            )
            return {}

        return self.extract_requested_attributes(attributes, data)

    def check_config(self) -> None:
        config = HaalCentraalHRConfig.get_solo()

        if not config.service:
            raise InvalidPluginConfiguration(_("Service not selected"))

        haal_centraal_hr_client = config.build_client()

        kvk_value = "TEST"
        try:
            haal_centraal_hr_client.retrieve(
                "RaadpleegMaatschappelijkeActiviteitOpKvKnummer",
                url=f"maatschappelijkeactiviteiten/{kvk_value}",
                request_kwargs={
                    "headers": {
                        "Accept": "application/hal+json",
                    },
                },
            )
        except ClientError as exc:
            if exc.args[0].get("status") == 400:
                return
            raise InvalidPluginConfiguration(
                _("Client error: {exception}").format(exception=exc)
            )
