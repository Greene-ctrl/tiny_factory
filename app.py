import sys
import os
import gradio as gr
import json
from tinytroupe.factory import TinyPersonFactory

# --- CHANGE 1: The function now accepts an optional API key. ---
def generate_personas(business_description, customer_profile, num_personas, blablador_api_key=None):
    """
    Generates a list of TinyPerson instances based on the provided inputs.
    It prioritizes the API key passed as an argument, but falls back to the
    environment variable if none is provided (for UI use).
    """
    # --- CHANGE 2: Logic to determine which key to use. ---
    # Use the key from the API call if provided, otherwise get it from the Space secrets.
    api_key_to_use = blablador_api_key or os.getenv("BLABLADOR_API_KEY")

    if not api_key_to_use:
        return {"error": "BLABLADOR_API_KEY not found. Please provide it in your API call or set it as a secret in the Space settings."}

    # Store the original state of the environment variable, if it exists
    original_key = os.getenv("BLABLADOR_API_KEY")
    
    try:
        # --- CHANGE 3: Securely set the correct environment variable for this request. ---
        # The underlying tinytroupe library will look for this variable.
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
        # --- CHANGE 4: A robust cleanup using a 'finally' block. ---
        # This ensures the environment is always restored to its original state,
        # whether the function succeeds or fails.
        if original_key is None:
            # If the variable didn't exist originally, remove it.
            if "BLABLADOR_API_KEY" in os.environ:
                del os.environ["BLABLADOR_API_KEY"]
        else:
            # If it existed, restore its original value.
            os.environ["BLABLADOR_API_KEY"] = original_key


with gr.Blocks() as demo:
    gr.Markdown("<h1>Tiny Persona Generator</h1>")
    with gr.Row():
        with gr.Column():
            business_description_input = gr.Textbox(label="What is your business about?", lines=5)
            customer_profile_input = gr.Textbox(label="Information about your customer profile", lines=5)
            num_personas_input = gr.Number(label="Number of personas to generate", value=1, minimum=1, step=1)
            
            # --- CHANGE 5: The API key input is now INVISIBLE. ---
            # It still exists, so the API endpoint is created, but it's hidden from UI users.
            blablador_api_key_input = gr.Textbox(
                label="Blablador API Key (for API client use)", 
                visible=False
            )

            generate_button = gr.Button("Generate Personas")
        with gr.Column():
            output_json = gr.JSON(label="Generated Personas")

    generate_button.click(
        fn=generate_personas,
        # --- CHANGE 6: Pass the invisible textbox to the function. ---
        inputs=[business_description_input, customer_profile_input, num_personas_input, blablador_api_key_input],
        outputs=output_json,
        api_name="generate_personas"
    )

if __name__ == "__main__":
    demo.queue().launch()