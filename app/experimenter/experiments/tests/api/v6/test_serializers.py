import json

from django.conf import settings
from django.test import TestCase
from mozilla_nimbus_shared import check_schema

from experimenter.experiments.api.v6.serializers import (
    NimbusExperimentSerializer,
    NimbusProbeSetSerializer,
)
from experimenter.experiments.models import NimbusExperiment
from experimenter.experiments.tests.factories import (
    NimbusExperimentFactory,
    NimbusProbeSetFactory,
)


class TestNimbusExperimentSerializer(TestCase):
    maxDiff = None

    def test_serializer_outputs_expected_schema_with_feature(self):
        probe_set = NimbusProbeSetFactory.create()
        experiment = NimbusExperimentFactory.create_with_status(
            NimbusExperiment.Status.ACCEPTED,
            firefox_min_version=NimbusExperiment.Version.FIREFOX_80,
            targeting_config_slug=NimbusExperiment.TargetingConfig.ALL_ENGLISH,
            channels=[
                NimbusExperiment.Channel.DESKTOP_NIGHTLY,
                NimbusExperiment.Channel.DESKTOP_BETA,
                NimbusExperiment.Channel.DESKTOP_RELEASE,
            ],
            probe_sets=[probe_set],
        )

        serializer = NimbusExperimentSerializer(experiment)
        experiment_data = serializer.data.copy()
        branches_data = [dict(b) for b in experiment_data.pop("branches")]
        self.assertDictEqual(
            experiment_data,
            {
                "application": experiment.application,
                "bucketConfig": {
                    "randomizationUnit": (
                        experiment.bucket_range.isolation_group.randomization_unit
                    ),
                    "namespace": experiment.bucket_range.isolation_group.namespace,
                    "start": experiment.bucket_range.start,
                    "count": experiment.bucket_range.count,
                    "total": experiment.bucket_range.isolation_group.total,
                },
                "endDate": None,
                "id": experiment.slug,
                "isEnrollmentPaused": False,
                "proposedDuration": experiment.proposed_duration,
                "proposedEnrollment": experiment.proposed_enrollment,
                "referenceBranch": experiment.reference_branch.slug,
                "schemaVersion": settings.NIMBUS_SCHEMA_VERSION,
                "slug": experiment.slug,
                "startDate": None,
                "targeting": (
                    'channel in ["Nightly", "Beta", "Release"] && '
                    "version|versionCompare('80.!') >= .! && localeLanguageCode == 'en'"
                ),
                "userFacingDescription": experiment.public_description,
                "userFacingName": experiment.name,
                "probeSets": [probe_set.slug],
            },
        )
        self.assertEqual(len(branches_data), 2)
        for branch in experiment.branches.all():
            self.assertIn(
                {
                    "slug": branch.slug,
                    "ratio": branch.ratio,
                    "feature": {
                        "featureId": experiment.feature_config.slug,
                        "enabled": branch.feature_enabled,
                        "value": json.loads(branch.feature_value),
                    },
                },
                branches_data,
            )

        check_schema("experiments/NimbusExperiment", serializer.data)

    def test_serializer_outputs_expected_schema_without_feature(self):
        experiment = NimbusExperimentFactory.create_with_status(
            NimbusExperiment.Status.ACCEPTED,
            feature_config=None,
        )
        serializer = NimbusExperimentSerializer(experiment)
        experiment_data = serializer.data.copy()
        branches_data = [dict(b) for b in experiment_data.pop("branches")]
        self.assertEqual(len(branches_data), 2)
        for branch in experiment.branches.all():
            self.assertIn(
                {"slug": branch.slug, "ratio": branch.ratio},
                branches_data,
            )

        check_schema("experiments/NimbusExperiment", serializer.data)

    def test_serializer_outputs_targeting_for_experiment_without_channels(self):
        experiment = NimbusExperimentFactory.create_with_status(
            NimbusExperiment.Status.DRAFT,
            firefox_min_version=NimbusExperiment.Version.FIREFOX_80,
            targeting_config_slug=NimbusExperiment.TargetingConfig.ALL_ENGLISH,
            channels=[],
        )

        serializer = NimbusExperimentSerializer(experiment)
        self.assertEqual(
            serializer.data["targeting"],
            "version|versionCompare('80.!') >= .! && localeLanguageCode == 'en'",
        )

    def test_serializer_outputs_targeting_for_experiment_without_firefox_min_version(
        self,
    ):
        experiment = NimbusExperimentFactory.create_with_status(
            NimbusExperiment.Status.DRAFT,
            firefox_min_version=None,
            targeting_config_slug=NimbusExperiment.TargetingConfig.ALL_ENGLISH,
            channels=[
                NimbusExperiment.Channel.DESKTOP_NIGHTLY,
                NimbusExperiment.Channel.DESKTOP_BETA,
                NimbusExperiment.Channel.DESKTOP_RELEASE,
            ],
        )

        serializer = NimbusExperimentSerializer(experiment)
        self.assertEqual(
            serializer.data["targeting"],
            'channel in ["Nightly", "Beta", "Release"] && localeLanguageCode == \'en\'',
        )


class TestNimbusProbeSetSerializer(TestCase):
    def test_outputs_expected_schema(self):
        probeset = NimbusProbeSetFactory()

        probeset_data = dict(NimbusProbeSetSerializer(probeset).data)
        probes_data = [dict(p) for p in probeset_data.pop("probes")]

        self.assertEqual(
            probeset_data,
            {
                "name": probeset.name,
                "slug": probeset.slug,
            },
        )
        self.assertEqual(len(probes_data), probeset.probes.count())
        for probe in probeset.probes.all():
            self.assertIn(
                {
                    "name": probe.name,
                    "kind": probe.kind,
                    "event_category": probe.event_category,
                    "event_method": probe.event_method,
                    "event_object": probe.event_object,
                    "event_value": probe.event_value,
                },
                probes_data,
            )