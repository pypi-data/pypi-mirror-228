import logging

from django.db import models
from django.utils.translation import gettext_lazy as _

from openforms.pre_requests.clients import PreRequestClientContext, PreRequestZGWClient
from openforms.submissions.models import Submission
from solo.models import SingletonModel
from zgw_consumers.constants import APITypes

logger = logging.getLogger(__name__)


class HaalCentraalHRConfigManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("service")


class HaalCentraalHRConfig(SingletonModel):
    """Configuration for the Haal Centraal HR Prefill"""

    service = models.OneToOneField(
        "zgw_consumers.Service",
        verbose_name=_("Haal Centraal HR API"),
        on_delete=models.PROTECT,
        limit_choices_to={"api_type": APITypes.orc},
        related_name="+",
        null=True,
    )

    objects = HaalCentraalHRConfigManager()

    class Meta:
        verbose_name = _("Haal Centraal HR configuration")

    def build_client(
        self, submission: Submission | None = None
    ) -> PreRequestZGWClient | None:
        if not self.service:
            logger.info("No service configured for Haal Centraal HR.")
            return

        client = self.service.build_client()
        if submission:
            client.context = PreRequestClientContext(submission=submission)

        return client
