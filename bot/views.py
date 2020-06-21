import json
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic import View
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.ext.django_chatterbot import settings
#from chatterbot.ext.django_chatterbot.models import Conversation, Response



class ChatterBotAppView(TemplateView):
    template_name = 'homepage.html'



class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """

    chatterbot = ChatBot(**settings.CHATTERBOT)

    trainer = ChatterBotCorpusTrainer(chatterbot)
    trainer.train("chatterbot.corpus.english")

    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.

        * The JSON data should contain a 'text' attribute.
        """
        data = json.loads(request.body.decode('utf-8'))

        if 'text' not in data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)

        response = self.chatterbot.get_response(data)

        response_data = response.serialize()

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        return JsonResponse({
            'name': self.chatterbot.name
        })


'''
chatbot = ChatBot('a-Bot')

conversation = [
    "Hello",
    "Hi there!",
    "How are you doing?",
    "I'm doing great.",
    "That is good to hear",
    "Thank you.",
    "You're welcome."
]
trainer = ListTrainer(chatbot)

trainer.train(conversation)

@csrf_exempt
def get_response(request):
	response = {'status': None}

	if request.method == 'POST':
		data = json.loads(request.body)
		message = data['message']

		chat_response = chatbot.get_response(message).text
		response['message'] = {'text': chat_response, 'user': False, 'chat_bot': True}
		response['status'] = 'ok'

	else:
		response['error'] = 'no POST data found'

	return HttpResponse(json.dumps(response), content_type="application/json")

def homepage(request):
	context = {'title': 'chatbot version 1.0'}
	return render(request, 'homepage.html', context)
'''