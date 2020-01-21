from django.test import TestCase
import datetime

from django.utils import timezone

from .models import Question

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(pub_date = time, question_text = question_text)



class QuestionDetailViewTests(TestCase):

    
    def test_nofuture(self):
        create_question(question_text= "future question", days= 30)
        response = self.client.get(reverse('polls:deatil', args = future_question.id))
        
        self.assertEqual(response.status_code,404)

    def test_normal(self):
        past_q= create_question(question_text= "past question", days= -5)
        response = self.client.get(reverse('polls:deatil', args = future_question.id))
        
        self.assertEqual(response,past_question.question_text)



class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

class QuestionModelTests(TestCase):
    def test_recent_publish_with_future(self):

        ''' should return false for questions with publish date in the future'''

        time = timezone.now()+datetime.timedelta(days=30)

        future_question = Question(pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_recent_correct(self):

        time = timezone.now() - datetime.timedelta(hours=5)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_old_not_recent(self):
        time = timezone.now() - datetime.timedelta(weeks=1)
        old = Question(pub_date = time)
        self.assertIs(old.was_published_recently(), False)
# Create your tests here.


