from django.views import View
from django.shortcuts import render, redirect
from django.conf import settings
import openai
from .models import ChaterSession, Message
from .forms import ChaterForm

openai.api_key = settings.OPENAI_API_KEY

class ChaterView(View):
    form_class = ChaterForm
    template_name = 'chater.html'

    def get_session(self, request):
        session_id = request.session.get('chater_session_id')

        # Check if session_id exists and is a valid UUID
        if session_id:
            try:
                session = ChaterSession.objects.get(session_id=session_id)
            except (ChaterSession.DoesNotExist, ValueError):
                # Handle cases where session_id is invalid
                session = ChaterSession.objects.create()
                request.session['chater_session_id'] = str(session.session_id)
        else:
            session = ChaterSession.objects.create()
            request.session['chater_session_id'] = str(session.session_id)

        return session

    def get(self, request, *args, **kwargs):
        session = self.get_session(request)
        messages = Message.objects.filter(session=session).order_by('timestamp')
        form = self.form_class()

        return render(request, self.template_name, {'form': form, 'messages': messages})

    def post(self, request, *args, **kwargs):
        session = self.get_session(request)

        form = self.form_class(request.POST)
        if form.is_valid():
            user_message = form.cleaned_data['message']
            Message.objects.create(session=session, content=user_message, is_user=True)

            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": user_message},
                ]
            )

            gpt_message = response.choices[0].message['content']
            Message.objects.create(session=session, content=gpt_message, is_user=False)

            return redirect('chater')  # Redirect to the same view to clear the form and avoid resubmission

        messages = Message.objects.filter(session=session).order_by('timestamp')
        return render(request, self.template_name, {'form': form, 'messages': messages})