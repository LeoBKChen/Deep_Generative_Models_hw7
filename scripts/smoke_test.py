from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.config import MOCK_MODE
from src.image_generator import DISABLED_STATUS, generate_tank_image
from src.prompt_generator import generate_design_prompt
from src.rag import retrieve
from src.report_generator import answer_question, generate_diagnosis_report
from src.turtle_profile import build_design_profile, build_diagnosis_profile, build_qa_profile


def assert_true(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    print("Running TurtleCare AI smoke test...")

    assert_true(MOCK_MODE is True, "Expected mock mode with the default local .env.")

    chunks = retrieve("Does my turtle need UVB light?", 3)
    assert_true(len(chunks) == 3, "RAG should return exactly 3 chunks.")
    assert_true(all("source" in chunk and "preview" in chunk for chunk in chunks), "RAG chunks need source and preview.")
    chinese_chunks = retrieve("我的烏龜需要 UVB 嗎？", 3)
    assert_true(
        any(chunk["source"] == "lighting_and_basking.md" for chunk in chinese_chunks),
        "Chinese UVB query should retrieve lighting_and_basking.md.",
    )

    qa_profile = build_qa_profile("Red-eared slider", 8)
    qa = answer_question(qa_profile, "Does it need UVB?")
    assert_true("Mock TurtleCare AI answer" in qa["answer"], "Q&A mock answer was not returned.")
    assert_true(len(qa["references"]) == 3, "Q&A should include 3 references.")
    qa_zh = answer_question(qa_profile, "我的烏龜需要 UVB 嗎？")
    assert_true("根據本地知識庫" in qa_zh["answer"], "Chinese Q&A mock answer should use Chinese.")

    diagnosis_profile = build_diagnosis_profile(
        "Red-eared slider",
        1,
        10,
        60,
        35,
        40,
        20,
        "否",
        "否",
        "heater",
        "none",
        "pellets and dried shrimp",
        "否",
        "recently not eating",
    )
    diagnosis = generate_diagnosis_report(diagnosis_profile)
    assert_true("Basking Area" in diagnosis["risk_summary"], "Diagnosis should flag missing basking area.")
    assert_true("UVB Lighting" in diagnosis["risk_summary"], "Diagnosis should flag missing UVB light.")

    design_profile = build_design_profile(
        "Musk turtle",
        75,
        45,
        45,
        18,
        "natural clean indoor aquarium",
        "dry basking platform, gentle ramp, filter",
        "sharp rocks, tiny gravel",
        False,
    )
    design = generate_design_prompt(design_profile)
    assert_true("turtle tank" in design["image_prompt"].lower(), "Design prompt should describe a turtle tank.")
    assert_true(len(design["references"]) == 3, "Design prompt should include 3 references.")

    image_path, image_status = generate_tank_image(design["image_prompt"])
    assert_true(image_path is None, "Image path should be None when image generation is disabled.")
    assert_true(image_status == DISABLED_STATUS, "Disabled image generation status mismatch.")

    print("Smoke test passed.")


if __name__ == "__main__":
    main()
