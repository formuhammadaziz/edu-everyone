from django.core.management.base import BaseCommand
from exams.models import ExamSet, Section, ReadingPassage, Question


LISTENING_QUESTIONS = [
    {
        'text': 'What is the main reason the student is visiting the office?',
        'a': 'To collect exam results',
        'b': 'To register for a new course',
        'c': 'To pay tuition fees',
        'd': 'To change accommodation',
        'correct': 'B',
    },
    {
        'text': 'When does the registration deadline end?',
        'a': 'Friday afternoon',
        'b': 'Thursday morning',
        'c': 'Wednesday evening',
        'd': 'Monday at noon',
        'correct': 'A',
    },
    {
        'text': 'What document does the student need to bring?',
        'a': 'Passport',
        'b': 'Student ID card',
        'c': 'Bank statement',
        'd': 'Letter of acceptance',
        'correct': 'B',
    },
    {
        'text': 'How much does the registration fee cost?',
        'a': '$50',
        'b': '$75',
        'c': '$100',
        'd': '$120',
        'correct': 'C',
    },
    {
        'text': 'Where should the student go to complete the registration?',
        'a': 'Room 204, second floor',
        'b': 'Main reception desk',
        'c': 'Room 101, ground floor',
        'd': 'The library building',
        'correct': 'A',
    },
]

READING_PASSAGE = """
The Role of Sleep in Learning and Memory

Scientists have long suspected that sleep plays a crucial role in the consolidation of memory—the process by which newly acquired information is transformed into long-term memory. Research over the past two decades has provided compelling evidence for this relationship, revealing that sleep is not merely a passive state of rest but an active process essential for cognitive function.

During sleep, the brain undergoes a series of complex processes that are thought to strengthen the neural connections formed during waking hours. The hippocampus, a brain region critical for memory formation, replays the events of the day during slow-wave sleep, effectively transferring information to the neocortex for long-term storage. This process, known as memory consolidation, appears to be particularly important for declarative memory—the type of memory that involves facts and events.

Research has shown that students who sleep after studying perform significantly better on memory tests than those who remain awake. In one well-known study, participants who learned a set of word pairs and then slept retained approximately 20% more information than those who stayed awake. The benefits of sleep were not limited to simple memorisation tasks; sleep also improved performance on complex problem-solving tasks that required creative thinking.

The relationship between sleep deprivation and academic performance is equally revealing. Students who consistently sleep fewer than seven hours per night show measurable declines in attention, working memory, and executive function. These cognitive impairments can persist even after a single night of poor sleep, underscoring the importance of regular, adequate sleep for optimal academic performance.

Despite this evidence, many students continue to sacrifice sleep in favour of additional study time, particularly during examination periods. This strategy may be counterproductive: the short-term gain in study hours is likely offset by the reduction in cognitive performance and memory consolidation that occurs with sleep deprivation. Educators and health professionals increasingly recommend that students prioritise sleep as a fundamental component of effective learning.
"""

READING_QUESTIONS = [
    {
        'text': 'According to the passage, what is memory consolidation?',
        'a': 'The process of forgetting old memories to make room for new ones',
        'b': 'The transformation of newly acquired information into long-term memory',
        'c': 'The ability to recall information without any sleep',
        'd': 'A technique used by students to memorise facts quickly',
        'correct': 'B',
    },
    {
        'text': 'Which brain region is described as critical for memory formation?',
        'a': 'The neocortex',
        'b': 'The cerebellum',
        'c': 'The hippocampus',
        'd': 'The prefrontal cortex',
        'correct': 'C',
    },
    {
        'text': 'In the study mentioned, how much more information did sleeping participants retain?',
        'a': 'Approximately 10%',
        'b': 'Approximately 15%',
        'c': 'Approximately 20%',
        'd': 'Approximately 25%',
        'correct': 'C',
    },
    {
        'text': 'What happens to students who sleep fewer than seven hours per night?',
        'a': 'They develop serious health problems',
        'b': 'They show declines in attention, working memory, and executive function',
        'c': 'They perform better under pressure during exams',
        'd': 'Their creativity and problem-solving skills improve',
        'correct': 'B',
    },
    {
        'text': 'What is the author\'s view on studying instead of sleeping before exams?',
        'a': 'It is an effective strategy for short-term memory improvement',
        'b': 'It should be encouraged by educators',
        'c': 'It is likely counterproductive',
        'd': 'It has no measurable effect on performance',
        'correct': 'C',
    },
]


class Command(BaseCommand):
    help = 'Create a sample IELTS practice exam with listening and reading sections'

    def handle(self, *args, **options):
        if ExamSet.objects.filter(title='IELTS Practice Test 1').exists():
            self.stdout.write(self.style.WARNING('Sample data already exists. Skipping.'))
            return

        exam_set = ExamSet.objects.create(
            title='IELTS Practice Test 1',
            description='A full IELTS Academic practice test with listening and reading sections.',
            is_active=True,
        )

        # Listening section
        listening = Section.objects.create(
            exam_set=exam_set,
            section_type='listening',
            title='Listening Test',
            duration_minutes=30,
            order=1,
        )
        for i, q in enumerate(LISTENING_QUESTIONS, 1):
            Question.objects.create(
                section=listening,
                question_number=i,
                question_type='mcq',
                question_text=q['text'],
                option_a=q['a'],
                option_b=q['b'],
                option_c=q['c'],
                option_d=q['d'],
                correct_answer=q['correct'],
            )

        # Reading section
        reading = Section.objects.create(
            exam_set=exam_set,
            section_type='reading',
            title='Reading Test',
            duration_minutes=60,
            order=2,
        )
        ReadingPassage.objects.create(
            section=reading,
            title='The Role of Sleep in Learning and Memory',
            passage_text=READING_PASSAGE.strip(),
            order=1,
        )
        for i, q in enumerate(READING_QUESTIONS, 1):
            Question.objects.create(
                section=reading,
                question_number=i,
                question_type='mcq',
                question_text=q['text'],
                option_a=q['a'],
                option_b=q['b'],
                option_c=q['c'],
                option_d=q['d'],
                correct_answer=q['correct'],
            )

        self.stdout.write(self.style.SUCCESS(
            f'Created "{exam_set.title}" with {len(LISTENING_QUESTIONS)} listening '
            f'and {len(READING_QUESTIONS)} reading questions.'
        ))
