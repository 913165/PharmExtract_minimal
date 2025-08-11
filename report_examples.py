"""Example pharmaceutical reports for training the structuring model.

This module contains curated examples of pharmaceutical reports with their
corresponding structured extractions. These examples are used for few-shot
learning with PharmExtract to train the model on proper categorization of
report sections into header, methodology, results, and conclusions components
with appropriate regulatory significance labels.

The examples cover various pharmaceutical document types including clinical trials,
adverse event reports, drug interaction studies, regulatory submissions, and
pharmacokinetic studies to provide comprehensive training coverage for the
pharmaceutical report structuring task.
"""

import textwrap
from enum import Enum

import langextract as lx


class ReportSectionType(Enum):
    HEADER = "document_header"
    METHODOLOGY = "methodology_body"
    RESULTS = "results_body"
    CONCLUSIONS = "conclusions_suffix"


def get_examples_for_model() -> list[lx.data.ExampleData]:
    """Examples that structure pharmaceutical reports into semantic sections.

    Returns:
        List of ExampleData objects containing pharmaceutical report examples
        with their corresponding structured extractions for training
        the language model.
    """
    return [
        lx.data.ExampleData(
            text=textwrap.dedent(
                """\
                STUDY TITLE: Phase II Randomized Trial of Drug ABC in Type 2 Diabetes
                PROTOCOL NUMBER: ABC-2024-001
                SPONSOR: PharmaCorp Inc.
                STUDY DESIGN: Randomized, double-blind, placebo-controlled

                OBJECTIVES:
                Primary: Evaluate efficacy of Drug ABC in reducing HbA1c
                Secondary: Assess safety and tolerability

                PATIENT POPULATION: 240 adults with Type 2 diabetes, HbA1c 7.5-10.5%
                INCLUSION CRITERIA: Age 18-75, inadequate glycemic control on metformin
                """
            ).rstrip(),
            extractions=[
                lx.data.Extraction(
                    extraction_text="STUDY TITLE: Phase II Randomized Trial of Drug ABC in Type 2 Diabetes",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Title",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="PROTOCOL NUMBER: ABC-2024-001",
                    extraction_class="document_header",
                    attributes={
                        "section": "Protocol Number",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="SPONSOR: PharmaCorp Inc.",
                    extraction_class="document_header",
                    attributes={
                        "section": "Sponsor",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="STUDY DESIGN: Randomized, double-blind, placebo-controlled",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Design",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="OBJECTIVES: Primary: Evaluate efficacy of Drug ABC in reducing HbA1c Secondary: Assess safety and tolerability",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Objectives",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="PATIENT POPULATION: 240 adults with Type 2 diabetes, HbA1c 7.5-10.5%",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Patient Population",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="INCLUSION CRITERIA: Age 18-75, inadequate glycemic control on metformin",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Inclusion Criteria",
                    },
                ),
            ],
        ),
        lx.data.ExampleData(
            text=textwrap.dedent(
                """\
                STUDY TITLE: Evaluation of Drug XYZ for Hypertension Treatment
                SPONSOR: HealthPharma Ltd.
                STUDY DESIGN: Open-label, multicenter trial

                OBJECTIVES:
                Primary: Determine the effect of Drug XYZ on systolic and diastolic blood pressure
                Secondary: Monitor adverse events and laboratory changes

                PATIENT POPULATION: 150 patients with essential hypertension
                EXCLUSION CRITERIA: Secondary hypertension, significant comorbidities
                """
            ).rstrip(),
            extractions=[
                lx.data.Extraction(
                    extraction_text="STUDY TITLE: Evaluation of Drug XYZ for Hypertension Treatment",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Title",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="SPONSOR: HealthPharma Ltd.",
                    extraction_class="document_header",
                    attributes={
                        "section": "Sponsor",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="STUDY DESIGN: Open-label, multicenter trial",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Design",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="OBJECTIVES: Primary: Determine the effect of Drug XYZ on systolic and diastolic blood pressure Secondary: Monitor adverse events and laboratory changes",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Objectives",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="PATIENT POPULATION: 150 patients with essential hypertension",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Patient Population",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="EXCLUSION CRITERIA: Secondary hypertension, significant comorbidities",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Exclusion Criteria",
                    },
                ),
            ],
        ),
        lx.data.ExampleData(
            text=textwrap.dedent(
                """\
                STUDY TITLE: Long-term Safety of Drug ABC in Diabetic Patients
                PROTOCOL NUMBER: ABC-2024-002
                SPONSOR: PharmaCorp Inc.
                STUDY DESIGN: Multicenter, open-label extension study

                OBJECTIVES:
                Primary: Assess long-term safety and tolerability of Drug ABC
                Secondary: Evaluate sustained efficacy in glycemic control

                PATIENT POPULATION: 180 patients with Type 2 diabetes, previously treated with Drug ABC
                """
            ).rstrip(),
            extractions=[
                lx.data.Extraction(
                    extraction_text="STUDY TITLE: Long-term Safety of Drug ABC in Diabetic Patients",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Title",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="PROTOCOL NUMBER: ABC-2024-002",
                    extraction_class="document_header",
                    attributes={
                        "section": "Protocol Number",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="SPONSOR: PharmaCorp Inc.",
                    extraction_class="document_header",
                    attributes={
                        "section": "Sponsor",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="STUDY DESIGN: Multicenter, open-label extension study",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Design",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="OBJECTIVES: Primary: Assess long-term safety and tolerability of Drug ABC Secondary: Evaluate sustained efficacy in glycemic control",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Objectives",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="PATIENT POPULATION: 180 patients with Type 2 diabetes, previously treated with Drug ABC",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Patient Population",
                    },
                ),
            ],
        ),
        lx.data.ExampleData(
            text=textwrap.dedent(
                """\
                STUDY TITLE: Drug Interaction Study of ABC and XYZ
                SPONSOR: InterPharma Inc.
                STUDY DESIGN: Randomized, open-label, two-treatment, two-period, crossover study

                OBJECTIVES:
                Primary: Evaluate the pharmacokinetic interaction between Drug ABC and Drug XYZ
                Secondary: Assess safety and tolerability of the combination

                SUBJECTS: 60 healthy volunteers
                """
            ).rstrip(),
            extractions=[
                lx.data.Extraction(
                    extraction_text="STUDY TITLE: Drug Interaction Study of ABC and XYZ",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Title",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="SPONSOR: InterPharma Inc.",
                    extraction_class="document_header",
                    attributes={
                        "section": "Sponsor",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="STUDY DESIGN: Randomized, open-label, two-treatment, two-period, crossover study",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Design",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="OBJECTIVES: Primary: Evaluate the pharmacokinetic interaction between Drug ABC and Drug XYZ Secondary: Assess safety and tolerability of the combination",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Objectives",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="SUBJECTS: 60 healthy volunteers",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Subjects",
                    },
                ),
            ],
        ),
        lx.data.ExampleData(
            text=textwrap.dedent(
                """\
                STUDY TITLE: Phase III Trial of Drug XYZ for Chronic Pain
                PROTOCOL NUMBER: XYZ-2024-005
                SPONSOR: PainRelief Pharma
                STUDY DESIGN: Multicenter, randomized, double-blind, placebo-controlled

                OBJECTIVES:
                Primary: Evaluate the efficacy of Drug XYZ in reducing chronic pain
                Secondary: Assess the impact on quality of life and functional status

                PATIENT POPULATION: 300 adults with chronic pain
                """
            ).rstrip(),
            extractions=[
                lx.data.Extraction(
                    extraction_text="STUDY TITLE: Phase III Trial of Drug XYZ for Chronic Pain",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Title",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="PROTOCOL NUMBER: XYZ-2024-005",
                    extraction_class="document_header",
                    attributes={
                        "section": "Protocol Number",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="SPONSOR: PainRelief Pharma",
                    extraction_class="document_header",
                    attributes={
                        "section": "Sponsor",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="STUDY DESIGN: Multicenter, randomized, double-blind, placebo-controlled",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Design",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="OBJECTIVES: Primary: Evaluate the efficacy of Drug XYZ in reducing chronic pain Secondary: Assess the impact on quality of life and functional status",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Objectives",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="PATIENT POPULATION: 300 adults with chronic pain",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Patient Population",
                    },
                ),
            ],
        ),
        lx.data.ExampleData(
            text=textwrap.dedent(
                """\
                STUDY TITLE: Safety and Efficacy of Combination Therapy with ABC and XYZ
                SPONSOR: ComboPharma Co.
                STUDY DESIGN: Randomized, double-blind, placebo-controlled trial

                OBJECTIVES:
                Primary: Determine the safety and efficacy of the ABC and XYZ combination
                Secondary: Evaluate individual drug contributions to overall efficacy

                PATIENT POPULATION: 250 patients with moderate to severe chronic pain
                """
            ).rstrip(),
            extractions=[
                lx.data.Extraction(
                    extraction_text="STUDY TITLE: Safety and Efficacy of Combination Therapy with ABC and XYZ",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Title",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="SPONSOR: ComboPharma Co.",
                    extraction_class="document_header",
                    attributes={
                        "section": "Sponsor",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="STUDY DESIGN: Randomized, double-blind, placebo-controlled trial",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Design",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="OBJECTIVES: Primary: Determine the safety and efficacy of the ABC and XYZ combination Secondary: Evaluate individual drug contributions to overall efficacy",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Objectives",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="PATIENT POPULATION: 250 patients with moderate to severe chronic pain",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Patient Population",
                    },
                ),
            ],
        ),
        lx.data.ExampleData(
            text=textwrap.dedent(
                """\
                STUDY TITLE: Pharmacokinetics of Drug ABC in Healthy Subjects
                SPONSOR: PharmaCorp Inc.
                STUDY DESIGN: Open-label, single-dose, randomized-sequence, two-treatment, two-period, crossover study

                OBJECTIVES:
                Primary: Assess the pharmacokinetics of Drug ABC
                Secondary: Evaluate the safety and tolerability of Drug ABC

                SUBJECTS: 48 healthy male and female volunteers
                """
            ).rstrip(),
            extractions=[
                lx.data.Extraction(
                    extraction_text="STUDY TITLE: Pharmacokinetics of Drug ABC in Healthy Subjects",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Title",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="SPONSOR: PharmaCorp Inc.",
                    extraction_class="document_header",
                    attributes={
                        "section": "Sponsor",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="STUDY DESIGN: Open-label, single-dose, randomized-sequence, two-treatment, two-period, crossover study",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Design",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="OBJECTIVES: Primary: Assess the pharmacokinetics of Drug ABC Secondary: Evaluate the safety and tolerability of Drug ABC",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Objectives",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="SUBJECTS: 48 healthy male and female volunteers",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Subjects",
                    },
                ),
            ],
        ),
        lx.data.ExampleData(
            text=textwrap.dedent(
                """\
                STUDY TITLE: Evaluation of Long-term Outcomes with Drug XYZ
                SPONSOR: HealthPharma Ltd.
                STUDY DESIGN: Multicenter, open-label, long-term extension study

                OBJECTIVES:
                Primary: Evaluate the long-term safety and efficacy of Drug XYZ
                Secondary: Assess impact on quality of life and diabetes management

                PATIENT POPULATION: 200 patients with Type 2 diabetes, previously enrolled in XYZ-2024-005
                """
            ).rstrip(),
            extractions=[
                lx.data.Extraction(
                    extraction_text="STUDY TITLE: Evaluation of Long-term Outcomes with Drug XYZ",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Title",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="SPONSOR: HealthPharma Ltd.",
                    extraction_class="document_header",
                    attributes={
                        "section": "Sponsor",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="STUDY DESIGN: Multicenter, open-label, long-term extension study",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Design",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="OBJECTIVES: Primary: Evaluate the long-term safety and efficacy of Drug XYZ Secondary: Assess impact on quality of life and diabetes management",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Objectives",
                    },
                ),
                lx.data.Extraction(
                    extraction_text="PATIENT POPULATION: 200 patients with Type 2 diabetes, previously enrolled in XYZ-2024-005",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Patient Population",
                    },
                ),
            ],
        ),
    ]
