from questionnaire.models import Question, QuestionSet
from fingerprint.models import Answer, Fingerprint
from fingerprint.services import findName

''' Slugs to check for emptyness 16.01.04 group '''
array_slugs = ['Copy_CERAD_Figures_0', 'Copy_Figures_from_the_Adult_Memory_and_Information_0',
    'Copy_Figures_subtest_from_Mental_Deterioration_Bat_0', 'Copy_Rey_Osterrieth_Complex_Figure_0',
    'Cube_Analysis_Test_of_the_Visual_Object_and_Space__0', 'Specify_any_other_tests_16_01_04_06']

def checkQuestionsEmpty():
    questions = Question.objects.filter(slug__in = array_slugs)

    answers = Answer.objects.filter(question__in = questions).exclude(data='')

    # we need to double check to ensure with don't have white spaces
    anyanswer = False
    for answer in answers:
        if answer.data.strip() != '':
            print findName(answer.fingerprint_id)
            anyanswer = True

    print "- Has answers into questions to delete ? "+str(anyanswer)

    return anyanswer

def removeQuestions():
    print "- Removing questions: "
    questions = Question.object.filter(slug__in = array_slugs)

    for question in question:
        print "Removing question "+str(question.number)
        question.delete()

def renumberQuestions():
    changemap = {
        '16.01.05': '16.01.04',
        '16.01.05.01': '16.01.04.01',
        '16.01.05.02': '16.01.04.02',
        '16.01.05.03': '16.01.04.03',
        '16.01.05.04': '16.01.04.04',
        '16.01.05.05': '16.01.04.05',
        '16.01.05.06': '16.01.04.06',

        '16.01.06': '16.01.05',
        '16.01.06.01': '16.01.05.01',
        '16.01.06.02': '16.01.05.02',
        '16.01.06.03': '16.01.05.03',
        '16.01.06.04': '16.01.05.04',
        '16.01.06.05': '16.01.05.05',

        '16.01.07': '16.01.06',
        '16.01.07.01': '16.01.06.01',
        '16.01.07.02': '16.01.06.02',
        '16.01.07.03': '16.01.06.03',
        '16.01.07.04': '16.01.06.04',
        '16.01.07.05': '16.01.06.05',
        '16.01.07.06': '16.01.06.06',
        '16.01.07.07': '16.01.06.07',

        '16.01.08': '16.01.07',
        '16.01.08.01': '16.01.07.01',
        '16.01.08.02': '16.01.07.02',
        '16.01.08.03': '16.01.07.03',
        '16.01.08.04': '16.01.07.04'
    }
    print "- Remapping questions: "
    try:
        # id 506 = adcohort_Neuropsychological_Tests
        questions = QuestionSet.objects.get(id=506).questions()

        for question in questions:
            if question.number in changemap:
                print "Changing number: "+question.number+" to: "+changemap[question.number]
                question.number = changemap[question.number]
                print question.number
                question.save()

    except:
        raise


has_answers = checkQuestionsEmpty()
if not has_answers:
    removeQuestions()
    renumberQuestions()


print "-- Done --"