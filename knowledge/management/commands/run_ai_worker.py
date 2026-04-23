import time
import requests
import json
from django.core.management.base import BaseCommand
from knowledge.models import SearchHistory

class Command(BaseCommand):
    help = 'Processes the AI queue and generates similar questions'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("AI Worker Active..."))
        
        while True:
            item = SearchHistory.objects.filter(is_queued=True).order_by('created_at').first()
            
            if item:
                self.stdout.write(f"\n[🔄] Thinking: '{item.query}'")
                
                # Gather document context
                context_str = "\n---\n".join([f"Title: {a.title}\nContent: {a.content}" for a in item.source_articles.all()])
                
                # 1. GENERATE THE MAIN ANSWER
                prompt = (
                    f"Task: Internal Support Bot. Context: {context_str}\n\n"
                    f"If the query '{item.query}' is very broad/vague, summarize it in 1 sentence and ask a helpful follow-up.\n"
                    f"If specific, answer using the context. Query: {item.query}"
                )

                try:
                    res = requests.post('http://localhost:11434/api/generate', json={
                        "model": "qwen2.5:0.5b", "prompt": prompt, "stream": False
                    })
                    item.ai_response = res.json().get('response')
                    item.is_queued = False
                    item.save()
                    self.stdout.write(self.style.SUCCESS(f"[✅] Answered: {item.id}"))

                    # 2. PROACTIVE CACHING: Generate 5 similar questions
                    sim_prompt = f"Generate 5 alternative ways a customer service rep might ask about: '{item.query}'. Return as a simple list."
                    sim_res = requests.post('http://localhost:11434/api/generate', json={
                        "model": "qwen2.5:0.5b", "prompt": sim_prompt, "stream": False
                    })
                    
                    # Create instant cache hits for those variations
                    sim_questions = sim_res.json().get('response', '').split('\n')
                    for q in sim_questions:
                        if q.strip():
                            SearchHistory.objects.get_or_create(
                                query=q.strip()[:499],
                                defaults={
                                    'ai_response': item.ai_response,
                                    'user_feedback': 1, # Pre-approve for cache hits
                                    'confidence_score': item.confidence_score
                                }
                            )
                    self.stdout.write(f"   └─ Pre-cached 5 variations.")

                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error: {e}"))
                    time.sleep(10)

            time.sleep(5)
