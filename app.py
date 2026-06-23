from __future__ import annotations

import gradio as gr

from src.image_generator import generate_tank_image
from src.prompt_generator import generate_design_prompt
from src.report_generator import answer_question, generate_diagnosis_report
from src.turtle_profile import build_design_profile, build_diagnosis_profile, build_qa_profile


SPECIES = [
    "台灣斑龜 Taiwan stripe-necked turtle",
    "紅耳龜 Red-eared slider",
    "非洲側頸龜 African side-necked turtle",
    "麝香龜 Musk turtle",
    "地圖龜 Map turtle",
    "其他 / 不確定",
]


def handle_qa(species, shell_length, question):
    profile = build_qa_profile(species, shell_length)
    result = answer_question(profile, question or "")
    return result["answer"], result["references_text"]


def handle_diagnosis(
    species,
    number_of_turtles,
    shell_length,
    tank_length,
    tank_width,
    tank_height,
    water_depth,
    has_basking_area,
    has_uvb_light,
    heating_equipment,
    filtration_method,
    feeding_content,
    mixed_species,
    current_concern,
):
    profile = build_diagnosis_profile(
        species,
        number_of_turtles,
        shell_length,
        tank_length,
        tank_width,
        tank_height,
        water_depth,
        has_basking_area,
        has_uvb_light,
        heating_equipment,
        filtration_method,
        feeding_content,
        mixed_species,
        current_concern,
    )
    result = generate_diagnosis_report(profile)
    return result["report"], result["risk_summary"], result["references_text"]


def handle_design(
    species,
    tank_length,
    tank_width,
    tank_height,
    water_depth,
    desired_style,
    required_elements,
    elements_to_avoid,
    generate_image_choice,
):
    profile = build_design_profile(
        species,
        tank_length,
        tank_width,
        tank_height,
        water_depth,
        desired_style,
        required_elements,
        elements_to_avoid,
        generate_image_choice == "是",
    )
    result = generate_design_prompt(profile)
    image_path = None
    status = "使用者未要求產生圖片。目前僅顯示圖片生成 Prompt。"
    if generate_image_choice == "是":
        image_path, status = generate_tank_image(result["image_prompt"])
    return (
        result["image_prompt"],
        result["negative_prompt"],
        result["materials"],
        result["safety_notes"],
        status,
        image_path,
        result["references_text"],
    )


with gr.Blocks(title="TurtleCare AI") as demo:
    gr.Markdown(
        "# TurtleCare AI\n"
        "RAG-based 烏龜飼養、龜缸診斷與龜缸設計助手。"
        "本工具不提供獸醫診斷；若症狀嚴重、持續或惡化，請諮詢合格爬蟲類獸醫。"
    )

    with gr.Tab("烏龜照護問答"):
        qa_species = gr.Dropdown(SPECIES, label="烏龜種類", value=SPECIES[0])
        qa_shell = gr.Number(label="背甲長度（cm）", value=8)
        qa_question = gr.Textbox(label="使用者問題", lines=4, placeholder="例如：我的烏龜需要多深的水？")
        qa_button = gr.Button("產生回答")
        qa_answer = gr.Textbox(label="生成回答", lines=12)
        qa_refs = gr.Textbox(label="檢索參考資料", lines=8)
        qa_button.click(handle_qa, [qa_species, qa_shell, qa_question], [qa_answer, qa_refs])

    with gr.Tab("龜缸環境診斷"):
        with gr.Row():
            d_species = gr.Dropdown(SPECIES, label="烏龜種類", value=SPECIES[0])
            d_count = gr.Number(label="烏龜數量", value=1)
            d_shell = gr.Number(label="背甲長度（cm）", value=8)
        with gr.Row():
            d_length = gr.Number(label="水缸長度（cm）", value=60)
            d_width = gr.Number(label="水缸寬度（cm）", value=35)
            d_height = gr.Number(label="水缸高度（cm）", value=40)
            d_depth = gr.Number(label="水深（cm）", value=18)
        with gr.Row():
            d_basking = gr.Radio(["是", "否"], label="是否有曬台", value="否")
            d_uvb = gr.Radio(["是", "否"], label="是否有 UVB 燈", value="否")
            d_mixed = gr.Radio(["否", "是"], label="是否混養", value="否")
        d_heating = gr.Textbox(label="加溫設備", placeholder="例如：加溫棒、陶瓷加熱燈")
        d_filter = gr.Textbox(label="過濾方式", placeholder="例如：外掛過濾、圓筒過濾、沒有")
        d_feeding = gr.Textbox(label="餵食內容", placeholder="例如：飼料、蔬菜、偶爾魚蝦")
        d_concern = gr.Textbox(label="目前擔心的狀況", lines=3)
        d_button = gr.Button("產生診斷報告")
        d_report = gr.Textbox(label="環境診斷報告", lines=14)
        d_risks = gr.Textbox(label="風險摘要", lines=8)
        d_refs = gr.Textbox(label="檢索參考資料", lines=8)
        d_button.click(
            handle_diagnosis,
            [
                d_species,
                d_count,
                d_shell,
                d_length,
                d_width,
                d_height,
                d_depth,
                d_basking,
                d_uvb,
                d_heating,
                d_filter,
                d_feeding,
                d_mixed,
                d_concern,
            ],
            [d_report, d_risks, d_refs],
        )

    with gr.Tab("龜缸設計與圖片生成"):
        with gr.Row():
            p_species = gr.Dropdown(SPECIES, label="烏龜種類", value=SPECIES[0])
            p_length = gr.Number(label="水缸長度（cm）", value=75)
            p_width = gr.Number(label="水缸寬度（cm）", value=45)
            p_height = gr.Number(label="水缸高度（cm）", value=45)
            p_depth = gr.Number(label="水深（cm）", value=22)
        p_style = gr.Textbox(label="想要的風格", placeholder="例如：自然風、簡潔室內教育展示風")
        p_required = gr.Textbox(label="必要元素", placeholder="例如：曬台、緩坡、UVB 燈、過濾器")
        p_avoid = gr.Textbox(label="避免元素", placeholder="例如：尖銳石頭、小碎石、不穩固堆石")
        p_image_choice = gr.Radio(["否", "是"], label="是否產生圖片", value="否")
        p_button = gr.Button("產生龜缸設計")
        p_prompt = gr.Textbox(label="英文圖片生成 Prompt", lines=8)
        p_negative = gr.Textbox(label="Negative Prompt", lines=5)
        p_materials = gr.Textbox(label="建議材料", lines=5)
        p_safety = gr.Textbox(label="安全提醒", lines=5)
        p_status = gr.Textbox(label="圖片生成狀態", lines=2)
        p_image = gr.Image(label="生成圖片（如果可用）", type="filepath")
        p_refs = gr.Textbox(label="檢索參考資料", lines=8)
        p_button.click(
            handle_design,
            [p_species, p_length, p_width, p_height, p_depth, p_style, p_required, p_avoid, p_image_choice],
            [p_prompt, p_negative, p_materials, p_safety, p_status, p_image, p_refs],
        )


if __name__ == "__main__":
    demo.launch()
