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
                EXCLUSION CRITERIA: Type 1 diabetes, severe renal impairment
                
                TREATMENT ARMS:
                Drug ABC 50mg daily (n=120)
                Placebo (n=120)
                
                EFFICACY RESULTS:
                Primary endpoint achieved with statistical significance (p<0.001).
                Mean HbA1c reduction: Drug ABC -1.2% vs Placebo -0.3%.
                Response rate (HbA1c <7%): Drug ABC 65% vs Placebo 18%.
                
                SAFETY RESULTS:
                Most common adverse events were mild gastrointestinal symptoms in 15% of Drug ABC patients vs 8% placebo.
                No serious adverse events were considered drug-related.
                Hypoglycemia rate: Drug ABC 5% vs Placebo 2%.
                
                CONCLUSIONS:
                Drug ABC demonstrated statistically significant and clinically meaningful reduction in HbA1c.
                Safety profile was acceptable with manageable gastrointestinal side effects.
                Results support progression to Phase III development.
                """
            ).rstrip(),
            extractions=[
                lx.data.Extraction(
                    extraction_text="STUDY TITLE: Phase II Randomized Trial of Drug ABC in Type 2 Diabetes",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Identification",
                        "study_phase": "Phase II",
                        "therapeutic_area": "endocrinology"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="PROTOCOL NUMBER: ABC-2024-001\nSPONSOR: PharmaCorp Inc.\nSTUDY DESIGN: Randomized, double-blind, placebo-controlled",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Administration",
                        "study_phase": "Phase II"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Primary: Evaluate efficacy of Drug ABC in reducing HbA1c\nSecondary: Assess safety and tolerability",
                    extraction_class="document_header",
                    attributes={
                        "section": "Objectives",
                        "study_phase": "Phase II"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="PATIENT POPULATION: 240 adults with Type 2 diabetes, HbA1c 7.5-10.5%",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Study Population",
                        "regulatory_significance": "notable"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="INCLUSION CRITERIA: Age 18-75, inadequate glycemic control on metformin",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Inclusion Criteria",
                        "regulatory_significance": "notable"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="EXCLUSION CRITERIA: Type 1 diabetes, severe renal impairment",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Exclusion Criteria",
                        "regulatory_significance": "notable"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Drug ABC 50mg daily (n=120)",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Treatment Arms",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Placebo (n=120)",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Treatment Arms",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Primary endpoint achieved with statistical significance (p<0.001).",
                    extraction_class="results_body",
                    attributes={
                        "section": "Primary Endpoint Results",
                        "endpoint_type": "primary",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Mean HbA1c reduction: Drug ABC -1.2% vs Placebo -0.3%.",
                    extraction_class="results_body",
                    attributes={
                        "section": "Primary Endpoint Results",
                        "endpoint_type": "primary",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Response rate (HbA1c <7%): Drug ABC 65% vs Placebo 18%.",
                    extraction_class="results_body",
                    attributes={
                        "section": "Secondary Endpoint Results",
                        "endpoint_type": "secondary",
                        "regulatory_significance": "significant"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Most common adverse events were mild gastrointestinal symptoms in 15% of Drug ABC patients vs 8% placebo.",
                    extraction_class="results_body",
                    attributes={
                        "section": "Safety Results",
                        "safety_grade": "Grade 1",
                        "regulatory_significance": "notable"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="No serious adverse events were considered drug-related.",
                    extraction_class="results_body",
                    attributes={
                        "section": "Safety Results",
                        "regulatory_significance": "significant"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Hypoglycemia rate: Drug ABC 5% vs Placebo 2%.",
                    extraction_class="results_body",
                    attributes={
                        "section": "Safety Results",
                        "safety_grade": "Grade 2",
                        "regulatory_significance": "notable"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Drug ABC demonstrated statistically significant and clinically meaningful reduction in HbA1c.\nSafety profile was acceptable with manageable gastrointestinal side effects.\nResults support progression to Phase III development.",
                    extraction_class="conclusions_suffix",
                    attributes={
                        "regulatory_significance": "critical"
                    },
                ),
            ],
        ),
        lx.data.ExampleData(
            text=textwrap.dedent(
                """\
                ADVERSE EVENT REPORT
                
                CASE IDENTIFICATION: AE-2024-12345
                REPORT DATE: January 15, 2025
                REPORTER: Dr. Sarah Johnson, Principal Investigator
                
                PATIENT DEMOGRAPHICS:
                Age: 45 years
                Sex: Female
                Weight: 68 kg
                Medical History: Hypertension (2 years)
                
                DRUG INFORMATION:
                Product: Drug XYZ 50mg tablets
                Indication: Hypertension
                Dose: 50mg twice daily
                Start Date: January 1, 2025
                
                EVENT DESCRIPTION:
                On day 7 of treatment, patient developed generalized erythematous rash covering approximately 30% of body surface area.
                Rash was accompanied by mild itching but no fever or systemic symptoms.
                
                CONCOMITANT MEDICATIONS:
                None reported at time of event
                
                ACTION TAKEN:
                Drug XYZ discontinued immediately
                Patient treated with topical corticosteroids and oral antihistamines
                
                OUTCOME:
                Complete resolution of rash within 5 days of drug discontinuation
                
                CAUSALITY ASSESSMENT:
                Investigator assessment: Probable relationship to Drug XYZ
                Rationale: Temporal relationship and positive dechallenge
                """
            ).rstrip(),
            extractions=[
                lx.data.Extraction(
                    extraction_text="ADVERSE EVENT REPORT\n\nCASE IDENTIFICATION: AE-2024-12345\nREPORT DATE: January 15, 2025\nREPORTER: Dr. Sarah Johnson, Principal Investigator",
                    extraction_class="document_header",
                    attributes={
                        "section": "Case Identification",
                        "therapeutic_area": "cardiovascular"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Age: 45 years\nSex: Female\nWeight: 68 kg\nMedical History: Hypertension (2 years)",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Patient Demographics",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Product: Drug XYZ 50mg tablets\nIndication: Hypertension\nDose: 50mg twice daily\nStart Date: January 1, 2025",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Drug Information",
                        "drug_class": "antihypertensive",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="On day 7 of treatment, patient developed generalized erythematous rash covering approximately 30% of body surface area.",
                    extraction_class="results_body",
                    attributes={
                        "section": "Adverse Event Description",
                        "safety_grade": "Grade 2",
                        "regulatory_significance": "significant"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Rash was accompanied by mild itching but no fever or systemic symptoms.",
                    extraction_class="results_body",
                    attributes={
                        "section": "Adverse Event Description",
                        "safety_grade": "Grade 1",
                        "regulatory_significance": "notable"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="None reported at time of event",
                    extraction_class="results_body",
                    attributes={
                        "section": "Concomitant Medications",
                        "regulatory_significance": "notable"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Drug XYZ discontinued immediately\nPatient treated with topical corticosteroids and oral antihistamines",
                    extraction_class="results_body",
                    attributes={
                        "section": "Action Taken",
                        "regulatory_significance": "significant"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Complete resolution of rash within 5 days of drug discontinuation",
                    extraction_class="results_body",
                    attributes={
                        "section": "Outcome",
                        "regulatory_significance": "significant"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Investigator assessment: Probable relationship to Drug XYZ\nRationale: Temporal relationship and positive dechallenge",
                    extraction_class="conclusions_suffix",
                    attributes={
                        "causality": "probable",
                        "regulatory_significance": "critical"
                    },
                ),
            ],
        ),
        lx.data.ExampleData(
            text=textwrap.dedent(
                """\
                DRUG INTERACTION STUDY REPORT
                
                STUDY OBJECTIVE: 
                To assess potential pharmacokinetic interactions between Drug A and Drug B when co-administered
                
                STUDY DESIGN:
                Open-label, randomized, crossover study in healthy volunteers
                Treatment periods separated by 7-day washout
                
                SUBJECTS:
                24 healthy adult volunteers (12 male, 12 female)
                Age range: 21-45 years
                
                TREATMENTS:
                Period 1: Drug A 100mg single dose
                Period 2: Drug A 100mg + Drug B 50mg single doses
                
                PHARMACOKINETIC RESULTS:
                Drug A alone: Cmax 150 ng/mL, AUC 800 ng*h/mL, t1/2 8 hours
                Drug A + Drug B: Cmax 185 ng/mL, AUC 1080 ng*h/mL, t1/2 12 hours
                
                INTERACTION ASSESSMENT:
                Co-administration resulted in 35% increase in Drug A AUC and 23% increase in Cmax
                Half-life prolonged by 50%
                
                CLINICAL SIGNIFICANCE:
                Moderate pharmacokinetic interaction requiring dose adjustment consideration
                Mechanism likely involves CYP3A4 inhibition by Drug B
                """
            ).rstrip(),
            extractions=[
                lx.data.Extraction(
                    extraction_text="DRUG INTERACTION STUDY REPORT\n\nSTUDY OBJECTIVE: \nTo assess potential pharmacokinetic interactions between Drug A and Drug B when co-administered",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Objective"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Open-label, randomized, crossover study in healthy volunteers\nTreatment periods separated by 7-day washout",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Study Design",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="24 healthy adult volunteers (12 male, 12 female)\nAge range: 21-45 years",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Study Population",
                        "regulatory_significance": "notable"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Period 1: Drug A 100mg single dose",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Treatment Regimen",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Period 2: Drug A 100mg + Drug B 50mg single doses",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Treatment Regimen",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Drug A alone: Cmax 150 ng/mL, AUC 800 ng*h/mL, t1/2 8 hours",
                    extraction_class="results_body",
                    attributes={
                        "section": "Pharmacokinetic Results",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Drug A + Drug B: Cmax 185 ng/mL, AUC 1080 ng*h/mL, t1/2 12 hours",
                    extraction_class="results_body",
                    attributes={
                        "section": "Pharmacokinetic Results",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Co-administration resulted in 35% increase in Drug A AUC and 23% increase in Cmax",
                    extraction_class="results_body",
                    attributes={
                        "section": "Interaction Assessment",
                        "regulatory_significance": "significant"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Half-life prolonged by 50%",
                    extraction_class="results_body",
                    attributes={
                        "section": "Interaction Assessment",
                        "regulatory_significance": "significant"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Moderate pharmacokinetic interaction requiring dose adjustment consideration\nMechanism likely involves CYP3A4 inhibition by Drug B",
                    extraction_class="conclusions_suffix",
                    attributes={
                        "regulatory_significance": "critical"
                    },
                ),
            ],
        ),
        lx.data.ExampleData(
            text=textwrap.dedent(
                """\
                REGULATORY SUBMISSION SUMMARY
                
                DRUG NAME: Generic Atorvastatin 20mg Tablets
                SUBMISSION TYPE: Abbreviated New Drug Application (ANDA)
                REFERENCE LISTED DRUG: Lipitor® 20mg Tablets
                THERAPEUTIC CATEGORY: HMG-CoA Reductase Inhibitor
                
                BIOEQUIVALENCE STUDY SUMMARY:
                Study design: Single-dose, randomized, crossover bioequivalence study
                Subjects: 36 healthy volunteers under fasted conditions
                
                QUALITY INFORMATION:
                Manufacturing site: FDA-approved facility with current GMP compliance
                Excipients: All excipients are compendial grade and previously approved
                
                BIOEQUIVALENCE RESULTS:
                Test formulation met bioequivalence criteria for both Cmax and AUC
                90% confidence intervals within 80-125% acceptance range
                Cmax ratio: 102.3% (95.1-109.8%)
                AUC ratio: 98.7% (94.2-103.4%)
                
                REGULATORY RECOMMENDATION:
                ANDA meets all regulatory requirements for approval
                Bioequivalence demonstrated with adequate safety margin
                Quality standards equivalent to reference product
                """
            ).rstrip(),
            extractions=[
                lx.data.Extraction(
                    extraction_text="REGULATORY SUBMISSION SUMMARY\n\nDRUG NAME: Generic Atorvastatin 20mg Tablets\nSUBMISSION TYPE: Abbreviated New Drug Application (ANDA)",
                    extraction_class="document_header",
                    attributes={
                        "section": "Submission Identification",
                        "therapeutic_area": "cardiovascular"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="REFERENCE LISTED DRUG: Lipitor® 20mg Tablets\nTHERAPEUTIC CATEGORY: HMG-CoA Reductase Inhibitor",
                    extraction_class="document_header",
                    attributes={
                        "section": "Drug Classification",
                        "drug_class": "statin",
                        "therapeutic_area": "cardiovascular"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Study design: Single-dose, randomized, crossover bioequivalence study\nSubjects: 36 healthy volunteers under fasted conditions",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Bioequivalence Study Design",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Manufacturing site: FDA-approved facility with current GMP compliance\nExcipients: All excipients are compendial grade and previously approved",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Quality Information",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Test formulation met bioequivalence criteria for both Cmax and AUC",
                    extraction_class="results_body",
                    attributes={
                        "section": "Bioequivalence Results",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="90% confidence intervals within 80-125% acceptance range",
                    extraction_class="results_body",
                    attributes={
                        "section": "Bioequivalence Results",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Cmax ratio: 102.3% (95.1-109.8%)",
                    extraction_class="results_body",
                    attributes={
                        "section": "Bioequivalence Results",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="AUC ratio: 98.7% (94.2-103.4%)",
                    extraction_class="results_body",
                    attributes={
                        "section": "Bioequivalence Results",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="ANDA meets all regulatory requirements for approval\nBioequivalence demonstrated with adequate safety margin\nQuality standards equivalent to reference product",
                    extraction_class="conclusions_suffix",
                    attributes={
                        "regulatory_significance": "critical"
                    },
                ),
            ],
        ),
        lx.data.ExampleData(
            text=textwrap.dedent(
                """\
                MANUFACTURING BATCH RECORD SUMMARY
                
                PRODUCT: Drug ABC 25mg Tablets
                BATCH NUMBER: ABC123456
                MANUFACTURING DATE: January 10, 2025
                EXPIRY DATE: January 2027
                
                BATCH SIZE: 100,000 tablets
                MANUFACTURING SITE: Facility XYZ (FDA Registration #12345678)
                
                RAW MATERIALS:
                All raw materials met release specifications
                Certificate of analysis reviewed and approved for each component
                
                IN-PROCESS CONTROLS:
                Tablet weight: Within ±5% specification limit
                Hardness: 6-12 kP (specification: 5-15 kP)
                Friability: 0.3% (specification: ≤1.0%)
                
                FINISHED PRODUCT TESTING:
                Assay: 101.2% (specification: 95.0-105.0%)
                Content uniformity: Passed (AV = 3.2, specification: ≤15.0)
                Dissolution: 98% at 30 minutes (specification: ≥80%)
                Microbiological limits: Compliant
                
                BATCH DISPOSITION:
                Batch approved for release and distribution
                All specifications met or exceeded
                """
            ).rstrip(),
            extractions=[
                lx.data.Extraction(
                    extraction_text="MANUFACTURING BATCH RECORD SUMMARY\n\nPRODUCT: Drug ABC 25mg Tablets\nBATCH NUMBER: ABC123456",
                    extraction_class="document_header",
                    attributes={
                        "section": "Batch Identification"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="MANUFACTURING DATE: January 10, 2025\nEXPIRY DATE: January 2027",
                    extraction_class="document_header",
                    attributes={
                        "section": "Batch Timeline"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="BATCH SIZE: 100,000 tablets\nMANUFACTURING SITE: Facility XYZ (FDA Registration #12345678)",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Manufacturing Information",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="All raw materials met release specifications\nCertificate of analysis reviewed and approved for each component",
                    extraction_class="results_body",
                    attributes={
                        "section": "Raw Materials Testing",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Tablet weight: Within ±5% specification limit",
                    extraction_class="results_body",
                    attributes={
                        "section": "In-Process Controls",
                        "regulatory_significance": "significant"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Hardness: 6-12 kP (specification: 5-15 kP)",
                    extraction_class="results_body",
                    attributes={
                        "section": "In-Process Controls",
                        "regulatory_significance": "significant"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Friability: 0.3% (specification: ≤1.0%)",
                    extraction_class="results_body",
                    attributes={
                        "section": "In-Process Controls",
                        "regulatory_significance": "significant"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Assay: 101.2% (specification: 95.0-105.0%)",
                    extraction_class="results_body",
                    attributes={
                        "section": "Finished Product Testing",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Content uniformity: Passed (AV = 3.2, specification: ≤15.0)",
                    extraction_class="results_body",
                    attributes={
                        "section": "Finished Product Testing",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Dissolution: 98% at 30 minutes (specification: ≥80%)",
                    extraction_class="results_body",
                    attributes={
                        "section": "Finished Product Testing",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Microbiological limits: Compliant",
                    extraction_class="results_body",
                    attributes={
                        "section": "Finished Product Testing",
                        "regulatory_significance": "significant"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Batch approved for release and distribution\nAll specifications met or exceeded",
                    extraction_class="conclusions_suffix",
                    attributes={
                        "regulatory_significance": "critical"
                    },
                ),
            ],
        ),
        lx.data.ExampleData(
            text=textwrap.dedent(
                """\
                PHARMACOKINETIC STUDY REPORT
                
                STUDY DESIGN: Single-dose, open-label PK study
                DRUG: Drug DEF 100mg oral tablet
                SUBJECTS: 24 healthy adult volunteers (12 male, 12 female)
                
                DOSING: Single 100mg dose administered after overnight fast
                SAMPLING: Blood samples collected over 48 hours post-dose
                ANALYTICAL METHOD: Validated LC-MS/MS method
                
                PHARMACOKINETIC PARAMETERS:
                Mean Cmax: 150 ± 25 ng/mL
                Median Tmax: 2.5 hours (range 1.5-4.0 hours)
                Mean AUC0-∞: 800 ± 120 ng*h/mL
                Mean elimination half-life: 8.2 ± 1.5 hours
                
                SAFETY ASSESSMENT:
                No serious adverse events reported
                Mild headache in 2 subjects, resolved spontaneously
                
                CONCLUSION:
                Drug DEF demonstrates predictable linear pharmacokinetics
                Elimination half-life supports once-daily dosing
                """
            ).rstrip(),
            extractions=[
                lx.data.Extraction(
                    extraction_text="PHARMACOKINETIC STUDY REPORT\n\nSTUDY DESIGN: Single-dose, open-label PK study\nDRUG: Drug DEF 100mg oral tablet",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Identification"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="SUBJECTS: 24 healthy adult volunteers (12 male, 12 female)",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Study Population",
                        "regulatory_significance": "notable"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="DOSING: Single 100mg dose administered after overnight fast\nSAMPLING: Blood samples collected over 48 hours post-dose\nANALYTICAL METHOD: Validated LC-MS/MS method",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Study Procedures",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Mean Cmax: 150 ± 25 ng/mL",
                    extraction_class="results_body",
                    attributes={
                        "section": "Pharmacokinetic Parameters",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Median Tmax: 2.5 hours (range 1.5-4.0 hours)",
                    extraction_class="results_body",
                    attributes={
                        "section": "Pharmacokinetic Parameters",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Mean AUC0-∞: 800 ± 120 ng*h/mL",
                    extraction_class="results_body",
                    attributes={
                        "section": "Pharmacokinetic Parameters",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Mean elimination half-life: 8.2 ± 1.5 hours",
                    extraction_class="results_body",
                    attributes={
                        "section": "Pharmacokinetic Parameters",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="No serious adverse events reported",
                    extraction_class="results_body",
                    attributes={
                        "section": "Safety Assessment",
                        "regulatory_significance": "significant"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Mild headache in 2 subjects, resolved spontaneously",
                    extraction_class="results_body",
                    attributes={
                        "section": "Safety Assessment",
                        "safety_grade": "Grade 1",
                        "regulatory_significance": "notable"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Drug DEF demonstrates predictable linear pharmacokinetics\nElimination half-life supports once-daily dosing",
                    extraction_class="conclusions_suffix",
                    attributes={
                        "regulatory_significance": "significant"
                    },
                ),
            ],
        ),
        lx.data.ExampleData(
            text=textwrap.dedent(
                """\
                STABILITY STUDY REPORT
                
                PRODUCT: Drug GHI 50mg Capsules
                STORAGE CONDITIONS: 25°C/60% RH (long-term) and 40°C/75% RH (accelerated)
                STUDY DURATION: 24 months (long-term), 6 months (accelerated)
                
                TEST PARAMETERS:
                Appearance, assay, dissolution, impurities, moisture content
                
                LONG-TERM STABILITY RESULTS (25°C/60% RH):
                Initial assay: 100.2%
                12 months: 99.8%
                24 months: 99.1%
                
                Dissolution maintained >85% throughout study period
                Total impurities remained <2.0% (specification: ≤3.0%)
                
                ACCELERATED STABILITY RESULTS (40°C/75% RH):
                6 months assay: 97.8%
                Slight increase in degradation products observed
                No significant change in dissolution profile
                
                SHELF LIFE RECOMMENDATION:
                Product remains stable for 24 months when stored at controlled room temperature
                No special storage requirements necessary
                """
            ).rstrip(),
            extractions=[
                lx.data.Extraction(
                    extraction_text="STABILITY STUDY REPORT\n\nPRODUCT: Drug GHI 50mg Capsules",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Identification"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="STORAGE CONDITIONS: 25°C/60% RH (long-term) and 40°C/75% RH (accelerated)\nSTUDY DURATION: 24 months (long-term), 6 months (accelerated)",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Study Conditions",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="TEST PARAMETERS:\nAppearance, assay, dissolution, impurities, moisture content",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Test Parameters",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Initial assay: 100.2%",
                    extraction_class="results_body",
                    attributes={
                        "section": "Long-term Stability Results",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="12 months: 99.8%",
                    extraction_class="results_body",
                    attributes={
                        "section": "Long-term Stability Results",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="24 months: 99.1%",
                    extraction_class="results_body",
                    attributes={
                        "section": "Long-term Stability Results",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Dissolution maintained >85% throughout study period",
                    extraction_class="results_body",
                    attributes={
                        "section": "Long-term Stability Results",
                        "regulatory_significance": "significant"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Total impurities remained <2.0% (specification: ≤3.0%)",
                    extraction_class="results_body",
                    attributes={
                        "section": "Long-term Stability Results",
                        "regulatory_significance": "significant"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="6 months assay: 97.8%",
                    extraction_class="results_body",
                    attributes={
                        "section": "Accelerated Stability Results",
                        "regulatory_significance": "significant"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Slight increase in degradation products observed",
                    extraction_class="results_body",
                    attributes={
                        "section": "Accelerated Stability Results",
                        "regulatory_significance": "notable"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="No significant change in dissolution profile",
                    extraction_class="results_body",
                    attributes={
                        "section": "Accelerated Stability Results",
                        "regulatory_significance": "significant"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Product remains stable for 24 months when stored at controlled room temperature\nNo special storage requirements necessary",
                    extraction_class="conclusions_suffix",
                    attributes={
                        "regulatory_significance": "critical"
                    },
                ),
            ],
        ),
        lx.data.ExampleData(
            text=textwrap.dedent(
                """\
                BIOEQUIVALENCE STUDY REPORT
                
                OBJECTIVE: Demonstrate bioequivalence between test and reference formulations of Drug JKL 100mg tablets
                
                STUDY DESIGN: Randomized, crossover, single-dose study under fasted conditions
                SUBJECTS: 36 healthy volunteers (18 male, 18 female)
                WASHOUT PERIOD: 14 days between treatments
                
                TEST PRODUCT: Generic Drug JKL 100mg tablets (Batch: GEN001)
                REFERENCE PRODUCT: Brand Drug JKL 100mg tablets (Batch: REF001)
                
                BIOANALYTICAL METHOD: Validated LC-MS/MS assay with LLOQ of 5 ng/mL
                
                PHARMACOKINETIC RESULTS:
                Test formulation Cmax: 485 ± 92 ng/mL
                Reference formulation Cmax: 478 ± 88 ng/mL
                
                Test formulation AUC0-t: 2150 ± 385 ng*h/mL
                Reference formulation AUC0-t: 2180 ± 402 ng*h/mL
                
                BIOEQUIVALENCE ANALYSIS:
                Cmax geometric mean ratio: 101.5% (90% CI: 96.2-106.9%)
                AUC0-t geometric mean ratio: 98.6% (90% CI: 94.1-103.4%)
                
                Both parameters within 80.00-125.00% acceptance criteria
                
                CONCLUSION:
                Bioequivalence successfully demonstrated
                Test product is therapeutically equivalent to reference product
                """
            ).rstrip(),
            extractions=[
                lx.data.Extraction(
                    extraction_text="BIOEQUIVALENCE STUDY REPORT\n\nOBJECTIVE: Demonstrate bioequivalence between test and reference formulations of Drug JKL 100mg tablets",
                    extraction_class="document_header",
                    attributes={
                        "section": "Study Objective"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="STUDY DESIGN: Randomized, crossover, single-dose study under fasted conditions\nSUBJECTS: 36 healthy volunteers (18 male, 18 female)\nWASHOUT PERIOD: 14 days between treatments",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Study Design",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="TEST PRODUCT: Generic Drug JKL 100mg tablets (Batch: GEN001)",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Study Products",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="REFERENCE PRODUCT: Brand Drug JKL 100mg tablets (Batch: REF001)",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Study Products",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="BIOANALYTICAL METHOD: Validated LC-MS/MS assay with LLOQ of 5 ng/mL",
                    extraction_class="methodology_body",
                    attributes={
                        "section": "Analytical Method",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Test formulation Cmax: 485 ± 92 ng/mL",
                    extraction_class="results_body",
                    attributes={
                        "section": "Pharmacokinetic Results",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Reference formulation Cmax: 478 ± 88 ng/mL",
                    extraction_class="results_body",
                    attributes={
                        "section": "Pharmacokinetic Results",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Test formulation AUC0-t: 2150 ± 385 ng*h/mL",
                    extraction_class="results_body",
                    attributes={
                        "section": "Pharmacokinetic Results",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Reference formulation AUC0-t: 2180 ± 402 ng*h/mL",
                    extraction_class="results_body",
                    attributes={
                        "section": "Pharmacokinetic Results",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Cmax geometric mean ratio: 101.5% (90% CI: 96.2-106.9%)",
                    extraction_class="results_body",
                    attributes={
                        "section": "Bioequivalence Analysis",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="AUC0-t geometric mean ratio: 98.6% (90% CI: 94.1-103.4%)",
                    extraction_class="results_body",
                    attributes={
                        "section": "Bioequivalence Analysis",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Both parameters within 80.00-125.00% acceptance criteria",
                    extraction_class="results_body",
                    attributes={
                        "section": "Bioequivalence Analysis",
                        "regulatory_significance": "critical"
                    },
                ),
                lx.data.Extraction(
                    extraction_text="Bioequivalence successfully demonstrated\nTest product is therapeutically equivalent to reference product",
                    extraction_class="conclusions_suffix",
                    attributes={
                        "regulatory_significance": "critical"
                    },
                ),
            ],
        ),
    ]