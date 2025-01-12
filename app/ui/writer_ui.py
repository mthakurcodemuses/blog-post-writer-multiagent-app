import gradio as gr
import requests
from app.core.config import settings

class WriterUI:
    def __init__(self):
        self.api_url = f"http://localhost:{settings.PORT}/api"
        self.thread_id = -1
        self.threads = []
        self.iterations = []
        
    def run_agent(self, start, topic, stop_after):
        if start:
            self.iterations.append(0)
            self.thread_id += 1
            self.threads.append(self.thread_id)
            state = {
                'task': topic,
                'max_revisions': 2,
                'revision_number': 0,
                'thread_id': self.thread_id
            }
        else:
            state = self._get_current_state()

        response = requests.post(f"{self.api_url}/generate", json=state)
        result = response.json()
        
        return (
            str(result), 
            result['node'],
            result['next_node'], 
            self.thread_id,
            result['revision']
        )

    def _get_current_state(self):
        response = requests.get(f"{self.api_url}/state/{self.thread_id}")
        return response.json()
    
    def create_interface(self):
        with gr.Blocks() as demo:
            with gr.Tab("Essay Writer"):
                with gr.Row():
                    topic = gr.Textbox(label="Essay Topic", value="What is AI?")
                    gen_btn = gr.Button("Generate Essay")
                    cont_btn = gr.Button("Continue")
                
                with gr.Row():
                    node = gr.Textbox(label="Current Node")
                    next_node = gr.Textbox(label="Next Node")
                    thread = gr.Textbox(label="Thread ID")
                    revision = gr.Textbox(label="Revision")
                
                output = gr.Textbox(label="Output", lines=10)
                
                gen_btn.click(
                    fn=self.run_agent,
                    inputs=[
                        gr.Number(True, visible=False),
                        topic,
                        gr.Textbox("", visible=False)
                    ],
                    outputs=[output, node, next_node, thread, revision]
                )
                
                cont_btn.click(
                    fn=self.run_agent,
                    inputs=[
                        gr.Number(False, visible=False),
                        topic,
                        gr.Textbox("", visible=False)
                    ],
                    outputs=[output, node, next_node, thread, revision]
                )
        
        return demo

    def launch(self):
        demo = self.create_interface()
        demo.launch(
            server_name="0.0.0.0",
            server_port=settings.UI_PORT,
            share=True
        )
