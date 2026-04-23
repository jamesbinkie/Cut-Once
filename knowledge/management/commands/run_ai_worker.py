import time
import requests
from django.core.management.base import BaseCommand
from knowledge.models import SearchHistory

class Command(BaseCommand):
    help = 'Runs the background AI worker to process queued search queries'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("AI Worker started! Listening for queued questions..."))
        
        while True:
            # 1. Find the oldest queued question
            queued_item = SearchHistory.objects.filter(is_queued=True).order_by('created_at').first()
            
            if queued_item:
                self.stdout.write(f"\n[🔄] Processing: '{queued_item.query}'...")
                
                # We need the document context. We grab it from the linked articles.
                context_texts = []
                for article in queued_item.source_articles.all():
                    context_texts.append(f"Title: {article.title}\nContent: {article.content}")
                
                context_str = "\n---\n".join(context_texts)
                
                # 2. Ask Ollama (No timeout limits here!)
                try:
                    response = requests.post('http://localhost:11434/api/generate', json={
                        "model": "qwen2.5:0.5b",
                        "prompt": f"Use ONLY this info: {context_str}\n\nQuestion: {queued_item.query}",
                        "stream": False
                    })
                    response.raise_for_status()
                    
                    ai_answer = response.json().get('response', 'Error: Empty response')
                    
                    # 3. Save the answer and remove from queue
                    queued_item.ai_response = ai_answer
                    queued_item.is_queued = False
                    queued_item.save()
                    
                    self.stdout.write(self.style.SUCCESS(f"[✅] Finished generating answer for: {queued_item.id}"))
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"[❌] Ollama failed: {e}"))
                    # We leave it in the queue so it tries again later
                    time.sleep(10) 

            # Wait 5 seconds before checking the database queue again
            time.sleep(5)
