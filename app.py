import sys
import os
import gradio as gr
import json
import random
from tinytroupe.factory import TinyPersonFactory
from tinytroupe.simulation_manager import SimulationConfig
from tinytroupe.content_generation import ContentVariantGenerator
from tinytroupe.agent_types import Content
from api.main import app, simulation_manager
import uvicorn

# --- CHANGE 1: The function now accepts an optional API key. ---
def generate_personas(business_description, customer_profile, num_personas, blablador_api_key=None):
    """
    Generates a list of TinyPerson instances based on the provided inputs.
    It prioritizes the API key passed as an argument, but falls back to the
    environment variable if none is provided (for UI use).
    """
    api_key_to_use = blablador_api_key or os.getenv("BLABLADOR_API_KEY")

    if not api_key_to_use:
        return {"error": "BLABLADOR_API_KEY not found. Please provide it in your API call or set it as a secret in the Space settings."}

    original_key = os.getenv("BLABLADOR_API_KEY")
    
    try:
        os.environ["BLABLADOR_API_KEY"] = api_key_to_use
        num_personas = int(num_personas)
        factory = TinyPersonFactory(
            context=business_description,
            sampling_space_description=customer_profile,
            total_population_size=num_personas
        )
        people = factory.generate_people(number_of_people=num_personas, parallelize=False)
        personas_data = [person._persona for person in people]
        return personas_data
    except Exception as e:
        return {"error": str(e)}
    finally:
        if original_key is None:
            if "BLABLADOR_API_KEY" in os.environ:
                del os.environ["BLABLADOR_API_KEY"]
        else:
            os.environ["BLABLADOR_API_KEY"] = original_key

def create_simulation_ui(name, persona_count, network_type):
    try:
        config = SimulationConfig(name=name, persona_count=int(persona_count), network_type=network_type)
        sim = simulation_manager.create_simulation(config)
        return {"status": "Simulation created", "id": sim.id, "persona_count": len(sim.personas)}
    except Exception as e:
        return {"error": str(e)}

def run_simulation_ui(simulation_id, content_text):
    try:
        if simulation_id not in simulation_manager.simulations:
            return {"error": "Simulation not found"}
        result = simulation_manager.run_simulation(simulation_id, content_text)
        return {
            "simulation_id": simulation_id,
            "total_reach": result.total_reach,
            "engagements": result.engagements
        }
    except Exception as e:
        return {"error": str(e)}

def predict_engagement_ui(persona_name, content_text, simulation_id):
    try:
        if simulation_id not in simulation_manager.simulations:
            return {"error": "Simulation not found"}
        sim = simulation_manager.simulations[simulation_id]
        persona = next((p for p in sim.personas if p.name == persona_name), None)
        if not persona:
            return {"error": "Persona not found"}

        content_obj = Content(text=content_text, content_type="post", topics=[], length=len(content_text), tone="")
        prob = sim.world._simulate_engagement_decision(persona, content_obj, 0)
        return {
            "persona": persona_name,
            "will_engage": prob.engaged,
            "probability": prob.probability,
            "comment": prob.comment
        }
    except Exception as e:
        return {"error": str(e)}

def generate_variants_ui(original_content, num_variants):
    try:
        variants = simulation_manager.variant_generator.generate_variants(original_content, int(num_variants))
        return [v.__dict__ for v in variants]
    except Exception as e:
        return {"error": str(e)}

def get_metrics_ui(simulation_id):
    try:
        if simulation_id not in simulation_manager.simulations:
            return {"error": "Simulation not found"}
        sim = simulation_manager.simulations[simulation_id]
        from tinytroupe.network_analysis import NetworkAnalyzer
        metrics = NetworkAnalyzer.calculate_centrality_metrics(sim.network)
        influencers = NetworkAnalyzer.identify_key_influencers(sim.network)
        return {
            "density": NetworkAnalyzer.calculate_density(sim.network),
            "key_influencers": influencers,
            "centrality_metrics": metrics
        }
    except Exception as e:
        return {"error": str(e)}


with gr.Blocks() as demo:
    gr.Markdown("<h1>Tiny Factory & Artificial Societies</h1>")

    with gr.Tabs():
        with gr.Tab("Persona Generation"):
            with gr.Row():
                with gr.Column():
                    business_description_input = gr.Textbox(label="What is your business about?", lines=5)
                    customer_profile_input = gr.Textbox(label="Information about your customer profile", lines=5)
                    num_personas_gen_input = gr.Number(label="Number of personas to generate", value=1, minimum=1, step=1)
                    blablador_api_key_input = gr.Textbox(label="Blablador API Key (for API client use)", visible=False)
                    generate_personas_button = gr.Button("Generate Personas")
                with gr.Column():
                    gen_personas_output = gr.JSON(label="Generated Personas")

            generate_personas_button.click(
                fn=generate_personas,
                inputs=[business_description_input, customer_profile_input, num_personas_gen_input, blablador_api_key_input],
                outputs=gen_personas_output,
                api_name="generate_personas"
            )

        with gr.Tab("Social Simulation"):
            with gr.Row():
                with gr.Column():
                    sim_name_input = gr.Textbox(label="Simulation Name", value="My Social Simulation")
                    sim_persona_count = gr.Number(label="Number of Personas", value=10, minimum=1, step=1)
                    sim_network_type = gr.Dropdown(label="Network Type", choices=["scale_free", "professional"], value="scale_free")
                    create_sim_button = gr.Button("Create Simulation")

                    sim_content_input = gr.Textbox(label="Content to Test", lines=3)
                    sim_id_run_input = gr.Textbox(label="Simulation ID (to run)")
                    run_sim_button = gr.Button("Run Content Spread Simulation")
                with gr.Column():
                    sim_output = gr.JSON(label="Simulation Status/Results")

            create_sim_button.click(
                fn=create_simulation_ui,
                inputs=[sim_name_input, sim_persona_count, sim_network_type],
                outputs=sim_output,
                api_name="create_simulation"
            )
            run_sim_button.click(
                fn=run_simulation_ui,
                inputs=[sim_id_run_input, sim_content_input],
                outputs=sim_output,
                api_name="run_simulation"
            )

        with gr.Tab("Engagement Prediction"):
            with gr.Row():
                with gr.Column():
                    pred_persona_name = gr.Textbox(label="Persona Name")
                    pred_content = gr.Textbox(label="Content Text", lines=3)
                    pred_sim_id = gr.Textbox(label="Simulation ID")
                    predict_button = gr.Button("Predict Engagement")
                with gr.Column():
                    pred_output = gr.JSON(label="Prediction Result")

            predict_button.click(
                fn=predict_engagement_ui,
                inputs=[pred_persona_name, pred_content, pred_sim_id],
                outputs=pred_output,
                api_name="predict_engagement"
            )

        with gr.Tab("Content Engine"):
            with gr.Row():
                with gr.Column():
                    cont_original = gr.Textbox(label="Original Content", lines=5)
                    cont_num_variants = gr.Number(label="Number of Variants", value=5, minimum=1)
                    generate_variants_button = gr.Button("Generate Variants")
                with gr.Column():
                    cont_output = gr.JSON(label="Content Variants")

            generate_variants_button.click(
                fn=generate_variants_ui,
                inputs=[cont_original, cont_num_variants],
                outputs=cont_output,
                api_name="generate_content_variants"
            )

        with gr.Tab("Network Analytics"):
            with gr.Row():
                with gr.Column():
                    metrics_sim_id = gr.Textbox(label="Simulation ID")
                    get_metrics_button = gr.Button("Get Network Metrics")
                with gr.Column():
                    metrics_output = gr.JSON(label="Network Analytics")

            get_metrics_button.click(
                fn=get_metrics_ui,
                inputs=[metrics_sim_id],
                outputs=metrics_output,
                api_name="get_network_metrics"
            )

# Mount Gradio app to FastAPI app imported from api.main
app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
