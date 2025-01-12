import gradio as gr
import os
import requests
from typing import Dict, Any

class EssayWriterUI:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self.current_thread_id = None
        self.demo = self.create_interface()

    def create_interface(self):
        """Create Gradio interface"""
        with gr.Blocks(theme=gr.themes.Default(spacing_size='sm',text_size="sm")) as demo:
            with gr.Tab("Agent"):
                with gr.Row():
                    topic_bx = gr.Textbox(label="Essay Topic", value="Pizza Shop")
                    gen_btn = gr.Button("Generate Essay", scale=0,min_width=80, variant='primary')
                    cont_btn = gr.Button("Continue Essay", scale=0,min_width=80)
                with gr.Row():
                    lnode_bx = gr.Textbox(label="last node", min_width=100)
                    nnode_bx = gr.Textbox(label="next node", min_width=100)
                    threadid_bx = gr.Textbox(label="Thread", scale=0, min_width=80)
                    revision_bx = gr.Textbox(label="Draft Rev", scale=0, min_width=80)
                    count_bx = gr.Textbox(label="count", scale=0, min_width=80)
                
                live = gr.Textbox(label="Live Agent Output", lines=5, max_lines=5)

                # Event handlers
                gen_btn.click(
                    fn=self.generate_essay,
                    inputs=[topic_bx],
                    outputs=[live, lnode_bx, nnode_bx, threadid_bx, revision_bx, count_bx]
                )
                
                cont_btn.click(
                    fn=self.continue_essay,
                    inputs=[],
                    outputs=[live, lnode_bx, nnode_bx, threadid_bx, revision_bx, count_bx]
                )

            with gr.Tab("Plan"):
                plan = gr.Textbox(label="Plan", lines=10, interactive=True)
                gr.Button("Refresh").click(
                    fn=self.get_state_value,
                    inputs=[],
                    outputs=[plan]
                )

            with gr.Tab("Draft"):
                draft = gr.Textbox(label="Draft", lines=10, interactive=True)
                gr.Button("Refresh").click(
                    fn=self.get_state_value,
                    inputs=[],
                    outputs=[draft]
                )

            with gr.Tab("Critique"):
                critique = gr.Textbox(label="Critique", lines=10, interactive=True)
                gr.Button("Refresh").click(
                    fn=self.get_state_value,
                    inputs=[],
                    outputs=[critique]
                )

        return demo

    def generate_essay(self, topic: str):
        """Generate new essay"""
        try:
            response = requests.post(
                f"{self.api_url}/essay",
                json={"topic": topic, "max_revisions": 2}
            )
            response.raise_for_status()
            data = response.json()
            self.current_thread_id = data["thread_id"]
            state = data["state"]
            return self._format_state_display(state)
        except Exception as e:
            return str(e), "", "", "", "", ""

    def continue_essay(self):
        """Continue existing essay"""
        try:
            if not self.current_thread_id:
                return "No active essay thread", "", "", "", "", ""
            
            response = requests.post(f"{self.api_url}/essay/{self.current_thread_id}/continue")
            response.raise_for_status()
            state = response.json()["state"]
            return self._format_state_display(state)
        except Exception as e:
            return str(e), "", "", "", "", ""

    def get_state_value(self, key: str = "plan"):
        """Get specific state value"""
        try:
            if not self.current_thread_id:
                return "No active essay thread"
            
            response = requests.get(f"{self.api_url}/essay/{self.current_thread_id}/state")
            response.raise_for_status()
            state = response.json()["state"]
            return state.get(key, "")
        except Exception as e:
            return str(e)

    def _format_state_display(self, state: Dict[str, Any]):
        """Format state for display"""
        display = f"Task: {state['task']}\n"
        display += f"Node: {state['lnode']}\n"
        display += f"Revision: {state['revision_number']}\n"
        
        return (
            display,
            state["lnode"],
            state.get("next_node", ""),
            self.current_thread_id,
            state["revision_number"],
            state["count"]
        )

    def launch(self):
        """Launch Gradio interface"""
        if port := os.getenv("PORT"):
            self.demo.launch(server_port=int(port), server_name="0.0.0.0")
        else:
            self.demo.launch(server_port=5000, server_name="0.0.0.0")
