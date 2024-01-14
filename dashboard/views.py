from django.shortcuts import render,redirect
from django.views import View
from django.contrib import messages
from .models import TdeeData
from django.contrib.auth.mixins import LoginRequiredMixin

def Home(request):
    titles = [
        'Mental health is just as important as physical health; prioritize self-care and seek support when needed.',
        'Consuming a variety of colorful fruits and vegetables provides a range of essential vitamins and minerals.',
        'Maintaining a healthy weight through diet and exercise is crucial for preventing obesity-related diseases.',
        'Moderate caffeine intake can enhance alertness, but excessive consumption may lead to negative health effects.',
        'Regular dental check-ups and oral hygiene practices are essential for overall health, preventing gum disease and infections.',
        'Bone density declines with age, making weight-bearing exercises crucial for maintaining bone health.',
        'The body circadian rhythm, influenced by sunlight, regulates sleep-wake cycles and overall well-being.',
        'Omega-3 fatty acids, found in fish and flaxseed, are beneficial for heart health and brain function.',
        'High levels of stress can negatively impact physical and mental health; practice stress-management techniques.',
        'Whole grains, rich in fiber, contribute to digestive health and can reduce the risk of chronic diseases.',
        'Regular stretching improves flexibility, reduces the risk of injury, and promotes better posture.',
        'Adequate sunlight exposure is essential for vitamin D synthesis, crucial for bone and immune health.',
        'Balancing different food groups ensures a diverse intake of nutrients for optimal health.',
        'Chronic inflammation is linked to various diseases; an anti-inflammatory diet can help reduce inflammation.',
        'Engaging in activities you enjoy boosts mental well-being and reduces the risk of depression.',
        'Maintaining proper posture supports spine health and reduces the risk of musculoskeletal issues.',
        'Chronic stress can contribute to weight gain; manage stress to support a healthy weight.',
        'Adequate water intake supports digestion, nutrient absorption, and overall bodily functions.',
        'Regular cardiovascular exercise enhances lung capacity and improves respiratory health.',
        'Mindful eating involves paying attention to food choices and savoring each bite, promoting healthier eating habits.',
        'Building and maintaining strong social connections is associated with a longer, healthier life.',
        'Maintaining a healthy gut microbiome through a balanced diet supports overall well-being.',
        'Moderation is key; balance indulgent treats with nutritious foods for a well-rounded diet.',
        'Regular health screenings, such as blood pressure and cholesterol checks, aid in early disease detection.',
        'Setting realistic and achievable fitness goals promotes motivation and long-term success.',
        'Mind-body practices like yoga and meditation can improve both physical and mental health.',
        'A good night sleep is essential for memory consolidation, emotional well-being, and overall health.',
        'Limiting alcohol consumption supports liver health and reduces the risk of alcohol-related diseases.',
        'Regular resistance training helps maintain muscle mass, strength, and overall functionality.',
        'Building healthy habits takes time; be patient and consistent for lasting improvements in well-being.',
        'Listening to your body hunger and fullness cues is crucial for maintaining a healthy weight.',
        'Social support is a powerful motivator; exercise with friends or join fitness classes for added encouragement.',
        'Practicing gratitude has positive effects on mental health and overall life satisfaction.',
        'Balancing work and leisure activities promotes a well-rounded and fulfilling life.',
    ]
    context = {
        'titles':titles
    }
    return render(request,'dashboard/index.html',context)

class TdeePage(LoginRequiredMixin,View):
    def get(self,request):
        context = {
            'recent_data':self.GetRecentData()
        }
        return render(request,'dashboard/tdee.html',context)
    
    def post(self,request):
        age = request.POST['age']
        gender = request.POST['gender']
        height = request.POST['height']
        weight = request.POST['weight']
        activityLevel = request.POST['activityLevel']
        context = {
            'FieldValues':request.POST,
            'recent_data':self.GetRecentData()
        }
        if int(age)<= 0 or int(height)<=0 or int(weight)<=0:
            messages.error(request,"Invalid input values. Age, height, and weight must be greater than 0.")
            return render(request,'dashboard/tdee.html',context)
        a = TdeeData.objects.create(
                user = request.user,
                age=age,
                gender=gender,
                height=height,
                weight=weight,
                activity_level=activityLevel
            )
        a.save()
        return redirect('main-tdee')
    
    def GetRecentData(self):
        return TdeeData.objects.filter(user=self.request.user).order_by('-created_at')[:4]

class NutritionPage(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'dashboard/nutrition.html')
    
    def post(self,request):
        pass

class MentalHealthPage(LoginRequiredMixin,View):
    questions_cat1 = [
            {
                'QID': 'MHQ011',
                'Question': "When exams stress you out, what do you usually do?",
                'Options': [
                    "Talk to a teacher or counsellor ",
                    "Make a study plan and stick to it ",
                    "Keep the stress to yourself",
                    "Avoid studying because it's too much"
                ],
                'Correct5': "Make a study plan and stick to it",
                'Correct3': "Talk to a teacher or counsellor"
            },
            {
                'QID': 'MHQ012',
                'Question': "If you're feeling sad, who would you want to talk to first?",
                'Options': [
                    "A close friend or family member ",
                    "A teacher or school counsellor ",
                    "Keep your feelings to yourself",
                    "Not sure or wouldn't talk to anyone"
                ],
                'Correct5': "A close friend or family member",
                'Correct3': "A teacher or school counsellor"
            },
            {
                'QID': 'MHQ013',
                'Question': "How do you balance schoolwork with relaxing?",
                'Options': [
                    "Take breaks and care for yourself ",
                    "Stick to a study plan and reward yourself ",
                    "Keep studying without breaks",
                    "Struggle to find a balance and feel overwhelmed"
                ],
                'Correct5': "Take breaks and care for yourself",
                'Correct3': "Stick to a study plan and reward yourself"
            },
            {
                'QID': 'MHQ014',
                'Question': "What do you prefer when it comes to working on school projects with others?",
                'Options': [
                    "Enjoy working with others ",
                    "Work with others but feel a bit nervous ",
                    "Prefer working alone",
                    "Feel very nervous and avoid group work"
                ],
                'Correct5': "Enjoy working with others",
                'Correct3': "Work with others but feel a bit nervous"
            },
            {
                'QID': 'MHQ015',
                'Question': "How do you handle changes or unexpected events in your routine?",
                'Options': [
                    "Adapt well and see them as opportunities ",
                    "Feel stressed at first but get used to it ",
                    "Struggle to adapt and like routine",
                    "Feel very anxious and find it hard to cope"
                ],
                'Correct5': "Adapt well and see them as opportunities",
                'Correct3': "Feel stressed at first but get used to it"
            },
            {
                'QID': 'MHQ016',
                'Question': "What's your plan for taking care of yourself during busy times?",
                'Options': [
                    "Make sure to get enough sleep and take breaks ",
                    "Sacrifice sleep to meet deadlines ",
                    "Forget self-care due to too much work",
                    "Often feel overwhelmed and neglect self-care"
                ],
                'Correct5': "Make sure to get enough sleep and take breaks",
                'Correct3': "Sacrifice sleep to meet deadlines"
            },
            {
                'QID': 'MHQ017',
                'Question': "If you see bullying at school, what would you do?",
                'Options': [
                    "Tell a teacher about it ",
                    "Try to help solve the problem ",
                    "Stay out of it to avoid trouble",
                    "Feel unsure how to respond"
                ],
                'Correct5': "Tell a teacher about it",
                'Correct3': "Try to help solve the problem"
            },
            {
                'QID': 'MHQ018',
                'Question': "How do you deal with not doing as well in school as you hoped?",
                'Options': [
                    "Get support from friends, family, or a counsellor ",
                    "Learn from mistakes and try harder ",
                    "Keep it to yourself and try to forget",
                    "Feel really discouraged and consider giving up"
                ],
                'Correct5': "Get support from friends, family, or a counsellor",
                'Correct3': "Learn from mistakes and try harder"
            },
            {
                'QID': 'MHQ019',
                'Question': "What's your sleep like during the school week?",
                'Options': [
                    "Get a good amount of sleep regularly ",
                    "Sometimes have trouble sleeping ",
                    "Often struggle to fall or stay asleep",
                    "Stay up very late or all night regularly"
                ],
                'Correct5': "Get a good amount of sleep regularly",
                'Correct3': "Sometimes have trouble sleeping"
            },
            {
                'QID': 'MHQ020',
                'Question': "How do you react to not doing well in school?",
                'Options': [
                    "Learn from mistakes and try again ",
                    "Feel disappointed but keep going ",
                    "Blame yourself and keep it inside",
                    "Feel overwhelmed and think about giving up"
                ],
                'Correct5': "Learn from mistakes and try again",
                'Correct3': "Feel disappointed but keep going"
            },
            {
                'QID': 'MHQ021',
                'Question': "How do you prepare for a big presentation at school?",
                'Options': [
                    "Practice in front of a mirror and seek feedback from peers ",
                    "Review your notes and hope for the best ",
                    "Avoid preparing and feel nervous about presenting",
                    "Skip the presentation altogether"
                ],
                'Correct5': "Practice in front of a mirror and seek feedback from peers",
                'Correct3': "Review your notes and hope for the best"
            },
            {
                'QID': 'MHQ022',
                'Question': "If you're feeling overwhelmed with schoolwork, what's your first step?",
                'Options': [
                    "Break down tasks into smaller parts and tackle them one by one ",
                    "Keep working continuously, hoping to finish everything ",
                    "Ignore the workload and hope it goes away",
                    "Feel too stressed to do anything about it"
                ],
                'Correct5': "Break down tasks into smaller parts and tackle them one by one",
                'Correct3': "Keep working continuously, hoping to finish everything"
            },
            {
                'QID': 'MHQ023',
                'Question': "How do you respond to a friend who seems upset?",
                'Options': [
                    "Ask them what's wrong and offer support ",
                    "Assume they'll share if they want to and give them space ",
                    "Ignore it and hope they feel better on their own",
                    "Feel unsure about how to approach them"
                ],
                'Correct5': "Ask them what's wrong and offer support",
                'Correct3': "Assume they'll share if they want to and give them space"
            },
            {
                'QID': 'MHQ024',
                'Question': "How do you handle conflicts with friends?",
                'Options': [
                    "Talk to your friend openly about the issue and find a solution together ",
                    "Give it time, and hope the issue resolves itself ",
                    "Avoid confronting your friend to prevent more problems",
                    "Feel upset but keep your feelings to yourself"
                ],
                'Correct5': "Talk to your friend openly about the issue and find a solution together",
                'Correct3': "Give it time, and hope the issue resolves itself"
            },
            {
                'QID': 'MHQ025',
                'Question': "When you're feeling down, what activity usually helps lift your spirits?",
                'Options': [
                    "Engaging in a favourite hobby or activity ",
                    "Watching TV or playing video games to distract yourself ",
                    "Doing nothing and waiting for the sadness to pass",
                    "Not sure, as nothing seems to help"
                ],
                'Correct5': "Engaging in a favourite hobby or activity",
                'Correct3': "Watching TV or playing video games to distract yourself"
            },
            {
                'QID': 'MHQ026',
                'Question': "How do you manage your time when juggling multiple assignments?",
                'Options': [
                    "Create a schedule and prioritize tasks based on deadlines ",
                    "Start working on whatever assignment feels easiest ",
                    "Procrastinate until the last minute",
                    "Feel overwhelmed and unsure where to start"
                ],
                'Correct5': "Create a schedule and prioritize tasks based on deadlines",
                'Correct3': "Start working on whatever assignment feels easiest"
            },
            {
                'QID': 'MHQ027',
                'Question': "What's your approach to handling peer pressure?",
                'Options': [
                    "Stick to your values and say no if it goes against them ",
                    "Sometimes give in to peer pressure, but not always ",
                    "Usually go along with what others want to fit in",
                    "Feel pressured but don't know how to respond"
                ],
                'Correct5': "Stick to your values and say no if it goes against them",
                'Correct3': "Sometimes give in to peer pressure, but not always"
            },
            {
                'QID': 'MHQ028',
                'Question': "How do you react when someone disagrees with you?",
                'Options': [
                    "Listen to their perspective and try to understand their point of view ",
                    "Stick to your opinion and avoid further discussion ",
                    "Get upset and argue your point aggressively",
                    "Feel uncomfortable and avoid disagreement"
                ],
                'Correct5': "Listen to their perspective and try to understand their point of view",
                'Correct3': "Stick to your opinion and avoid further discussion"
            },
            {
                'QID': 'MHQ029',
                'Question': "How do you handle a situation where you make a mistake in front of others?",
                'Options': [
                    "Acknowledge the mistake, learn from it, and move on ",
                    "Downplay the mistake and hope no one notices ",
                    "Feel embarrassed and try to avoid the situation",
                    "Blame others for the mistake"
                ],
                'Correct5': "Acknowledge the mistake, learn from it, and move on",
                'Correct3': "Downplay the mistake and hope no one notices"
            },
            {
                'QID': 'MHQ030',
                'Question': "When you're feeling stressed, what's your go-to relaxation method?",
                'Options': [
                    "Deep breathing exercises or mindfulness ",
                    "Distract yourself with TV or social media ",
                    "Try to push through the stress without taking a break",
                    "Feel too overwhelmed to relax"
                ],
                'Correct5': "Deep breathing exercises or mindfulness",
                'Correct3': "Distract yourself with TV or social media"
            }
    ]

    questions_cat2 = [
        {
            'QID': 'MHQ031',
            'Question': "How do you typically manage work-related stress?",
            'Options': [
                "Utilize stress management techniques and communicate with colleagues or supervisors ",
                "Push through the stress, hoping it will get better with time ",
                "Keep stress to yourself and avoid discussing it with others",
                "Ignore work-related stress and hope it goes away"
            ],
            'Correct5': "Utilize stress management techniques and communicate with colleagues or supervisors",
            'Correct3': "Push through the stress, hoping it will get better with time"
        },
        {
            'QID': 'MHQ032',
            'Question': "If you're feeling overwhelmed with personal commitments, what's your first step?",
            'Options': [
                "Prioritize tasks and delegate when possible ",
                "Keep trying to handle everything on your own ",
                "Ignore some responsibilities and hope they resolve themselves",
                "Feel too stressed to address the commitments"
            ],
            'Correct5': "Prioritize tasks and delegate when possible",
            'Correct3': "Keep trying to handle everything on your own"
        },
        {
            'QID': 'MHQ033',
            'Question': "How do you approach making decisions about your career path?",
            'Options': [
                "Set clear goals, research options, and seek advice from mentors ",
                "Go with the flow, taking opportunities as they come ",
                "Avoid making long-term career decisions",
                "Feel unsure and overwhelmed about career choices"
            ],
            'Correct5': "Set clear goals, research options, and seek advice from mentors",
            'Correct3': "Go with the flow, taking opportunities as they come"
        },
        {
            'QID': 'MHQ034',
            'Question': "When facing a setback in your personal life, how do you cope?",
            'Options': [
                "Seek support from friends, family, or a counsellor ",
                "Reflect on the situation, learn from it, and move forward ",
                "Keep emotions to yourself and try to handle it independently",
                "Withdraw from others and avoid dealing with the setback"
            ],
            'Correct5': "Seek support from friends, family, or a counsellor",
            'Correct3': "Reflect on the situation, learn from it, and move forward"
        },
        {
            'QID': 'MHQ035',
            'Question': "How do you handle conflicts in your relationships?",
            'Options': [
                "Communicate openly, listen actively, and work towards a resolution ",
                "Give it time and hope the issue resolves itself ",
                "Avoid confrontation to maintain peace",
                "Feel overwhelmed and unsure how to address conflicts"
            ],
            'Correct5': "Communicate openly, listen actively, and work towards a resolution",
            'Correct3': "Give it time and hope the issue resolves itself"
        },
        {
            'QID': 'MHQ036',
            'Question': "When it comes to setting personal goals, what's your approach?",
            'Options': [
                "Set specific, measurable goals and create a plan to achieve them ",
                "Have general ideas of what you want without a concrete plan ",
                "Avoid setting goals to prevent potential failure",
                "Feel uncertain about what you want to achieve"
            ],
            'Correct5': "Set specific, measurable goals and create a plan to achieve them",
            'Correct3': "Have general ideas of what you want without a concrete plan"
        },
        {
            'QID': 'MHQ037',
            'Question': "How do you prioritize self-care in your daily life?",
            'Options': [
                "Make time for regular self-care activities, such as exercise and relaxation ",
                "Occasionally engage in self-care activities when time allows ",
                "Neglect self-care due to a busy schedule",
                "Feel unsure about what constitutes self-care"
            ],
            'Correct5': "Make time for regular self-care activities, such as exercise and relaxation",
            'Correct3': "Occasionally engage in self-care activities when time allows"
        },
        {
            'QID': 'MHQ038',
            'Question': "What's your approach to managing financial responsibilities?",
            'Options': [
                "Create a budget, track expenses, and plan for future financial goals ",
                "Spend without a clear budget, hoping for the best ",
                "Avoid dealing with finances and hope they work out on their own",
                "Feel overwhelmed and anxious about financial responsibilities"
            ],
            'Correct5': "Create a budget, track expenses, and plan for future financial goals",
            'Correct3': "Spend without a clear budget, hoping for the best"
        },
        {
            'QID': 'MHQ039',
            'Question': "How do you react when facing uncertainties or unexpected changes in life?",
            'Options': [
                "Embrace change as an opportunity for growth and adapt accordingly ",
                "Feel uneasy but eventually adapt to new circumstances ",
                "Resist change and prefer stability",
                "Experience high anxiety and struggle to cope with uncertainties"
            ],
            'Correct5': "Embrace change as an opportunity for growth and adapt accordingly",
            'Correct3': "Feel uneasy but eventually adapt to new circumstances"
        },
        {
            'QID': 'MHQ040',
            'Question': "How do you manage your work-life balance?",
            'Options': [
                "Set boundaries, prioritize personal time, and avoid overworking ",
                "Often work long hours but find time for personal activities ",
                "Neglect personal time due to a heavy workload",
                "Feel unsure about how to balance work and personal life"
            ],
            'Correct5': "Set boundaries, prioritize personal time, and avoid overworking",
            'Correct3': "Often work long hours but find time for personal activities"
        },
        {
            'QID': 'MHQ041',
            'Question': "How do you approach networking and building professional connections?",
            'Options': [
                "Actively seek networking opportunities and cultivate professional relationships ",
                "Network occasionally but rely more on individual skills and experience ",
                "Avoid networking, believing that skills alone will pave the way",
                "Feel unsure about how to navigate professional relationships"
            ],
            'Correct5': "Actively seek networking opportunities and cultivate professional relationships",
            'Correct3': "Network occasionally but rely more on individual skills and experience"
        },
        {
            'QID': 'MHQ042',
            'Question': "When you encounter setbacks in your academic or professional pursuits, what's your response?",
            'Options': [
                "Analyse the situation, learn from the setback, and adjust your approach ",
                "Feel disappointed but keep going, hoping things will improve ",
                "Become discouraged and 'question' your abilities",
                "Avoid pursuing further goals to prevent future setbacks"
            ],
            'Correct5': "Analyse the situation, learn from the setback, and adjust your approach",
            'Correct3': "Feel disappointed but keep going, hoping things will improve"
        },
        {
            'QID': 'MHQ043',
            'Question': "How do you prioritize mental health in your daily routine?",
            'Options': [
                "Incorporate mindfulness or meditation practices and prioritize mental well-being ",
                "Occasionally engage in activities for mental well-being but not consistently ",
                "Neglect mental health due to a busy schedule",
                "Feel unsure about how to prioritize mental health"
            ],
            'Correct5': "Incorporate mindfulness or meditation practices and prioritize mental well-being",
            'Correct3': "Occasionally engage in activities for mental well-being but not consistently"
        },
        {
            'QID': 'MHQ044',
            'Question': "What's your approach to handling disagreements or conflicts at work?",
            'Options': [
                "Communicate openly, seek compromise, and work towards resolution ",
                "Let time pass, hoping the issue will resolve itself ",
                "Avoid addressing conflicts to maintain a harmonious work environment",
                "Feel overwhelmed and unsure how to handle workplace conflicts"
            ],
            'Correct5': "Communicate openly, seek compromise, and work towards resolution",
            'Correct3': "Let time pass, hoping the issue will resolve itself"
        },
        {
            'QID': 'MHQ045',
            'Question': "How do you stay motivated to achieve long-term goals in your personal or professional life?",
            'Options': [
                "Break goals into smaller tasks, celebrate achievements, and stay focused ",
                "Keep goals in mind but sometimes lack motivation to pursue them consistently ",
                "Avoid setting long-term goals to prevent potential disappointment",
                "Feel uncertain about setting and achieving long-term goals"
            ],
            'Correct5': "Break goals into smaller tasks, celebrate achievements, and stay focused",
            'Correct3': "Keep goals in mind but sometimes lack motivation to pursue them consistently"
        },
        {
            'QID': 'MHQ046',
            'Question': "How do you manage your digital well-being and screen time?",
            'Options': [
                "Set limits on screen time, take breaks, and prioritize face-to-face interactions ",
                "Use technology without strict limits but try to balance screen time ",
                "Neglect setting limits on screen time and use technology excessively",
                "Feel unsure about how to manage digital well-being"
            ],
            'Correct5': "Set limits on screen time, take breaks, and prioritize face-to-face interactions",
            'Correct3': "Use technology without strict limits but try to balance screen time"
        },
        {
            'QID': 'MHQ047',
            'Question': "When it comes to personal development, how do you seek continuous improvement?",
            'Options': [
                "Engage in regular learning, seek feedback, and actively pursue personal growth ",
                "Occasionally explore new opportunities for improvement but not consistently ",
                "Avoid seeking personal development opportunities",
                "Feel unsure about how to approach personal development"
            ],
            'Correct5': "Engage in regular learning, seek feedback, and actively pursue personal growth",
            'Correct3': "Occasionally explore new opportunities for improvement but not consistently"
        },
        {
            'QID': 'MHQ048',
            'Question': "How do you handle challenges related to time management and productivity?",
            'Options': [
                "Prioritize tasks, use time management tools, and set clear goals ",
                "Manage time reasonably well but occasionally struggle with productivity ",
                "Neglect time management and often feel overwhelmed",
                "Feel unsure about effective time management strategies"
            ],
            'Correct5': "Prioritize tasks, use time management tools, and set clear goals",
            'Correct3': "Manage time reasonably well but occasionally struggle with productivity"
        },
        {
            'QID': 'MHQ049',
            'Question': "How do you approach maintaining a healthy work-life-social balance?",
            'Options': [
                "Set clear boundaries, allocate time for work, personal life, and socializing ",
                "Prioritize work but find time for personal and social activities ",
                "Neglect personal and social activities due to work commitments",
                "Feel unsure about how to balance work, personal life, and socializing"
            ],
            'Correct5': "Set clear boundaries, allocate time for work, personal life, and socializing",
            'Correct3': "Prioritize work but find time for personal and social activities"
        },
        {
            'QID': 'MHQ050',
            'Question': "When planning for the future, how do you approach setting financial goals?",
            'Options': [
                "Create a detailed financial plan, set savings goals, and invest strategically ",
                "Have general financial goals but lack a specific plan ",
                "Avoid setting financial goals and hope for the best",
                "Feel uncertain about financial goal-setting and planning"
            ],
            'Correct5': "Create a detailed financial plan, set savings goals, and invest strategically",
            'Correct3': "Have general financial goals but lack a specific plan"
        }
    ]
    questions_cat3 = [
        {
            'QID': 'MHQ051',
            'Question': "How do you prioritize your mental health and well-being in your daily routine?",
            'Options': [
                "Incorporate mindful practices, prioritize self-care, and seek professional support when needed ",
                "Occasionally engage in activities for mental well-being but not consistently ",
                "Neglect mental health due to various responsibilities",
                "Feel unsure about how to prioritize mental health in your current stage of life"
            ],
            'Correct5': "Incorporate mindful practices, prioritize self-care, and seek professional support when needed",
            'Correct3': "Occasionally engage in activities for mental well-being but not consistently"
        },
        {
            'QID': 'MHQ052',
            'Question': "When faced with a significant career decision, how do you approach it?",
            'Options': [
                "Evaluate potential options, consider long-term implications, and seek advice from mentors ",
                "Go with the flow, taking opportunities as they come, but without a concrete plan ",
                "Avoid making long-term career decisions, feeling content with the present",
                "Feel uncertain about the best approach to career decisions at this stage"
            ],
            'Correct5': "Evaluate potential options, consider long-term implications, and seek advice from mentors",
            'Correct3': "Go with the flow, taking opportunities as they come, but without a concrete plan"
        },
        {
            'QID': 'MHQ053',
            'Question': "How do you navigate personal relationships and prioritize them in your busy life?",
            'Options': [
                "Communicate openly, set boundaries, and allocate quality time for loved ones ",
                "Maintain relationships but struggle with finding enough time for loved ones ",
                "Prioritize personal relationships over other commitments",
                "Feel uncertain about balancing personal relationships in your current stage of life"
            ],
            'Correct5': "Communicate openly, set boundaries, and allocate quality time for loved ones",
            'Correct3': "Maintain relationships but struggle with finding enough time for loved ones"
        },
        {
            'QID': 'MHQ054',
            'Question': "When managing finances, what's your approach to long-term financial planning?",
            'Options': [
                "Create a comprehensive financial plan, set clear goals, and invest strategically ",
                "Have general financial goals but lack a specific plan ",
                "Rely on short-term financial decisions without a long-term plan",
                "Feel uncertain about effective long-term financial planning"
            ],
            'Correct5': "Create a comprehensive financial plan, set clear goals, and invest strategically",
            'Correct3': "Have general financial goals but lack a specific plan"
        },
        {
            'QID': 'MHQ055',
            'Question': "How do you handle setbacks and challenges in your personal and professional life?",
            'Options': [
                "Analyse the situation, learn from setbacks, and adjust your approach ",
                "Bounce back from setbacks but sometimes feel the impact on your confidence ",
                "Struggle to recover from setbacks and feel discouraged",
                "Feel uncertain about how to effectively handle setbacks at this stage"
            ],
            'Correct5': "Analyse the situation, learn from setbacks, and adjust your approach",
            'Correct3': "Bounce back from setbacks but sometimes feel the impact on your confidence"
        },
        {
            'QID': 'MHQ056',
            'Question': "How do you approach maintaining a healthy work-life balance as responsibilities evolve?",
            'Options': [
                "Set clear boundaries, prioritize self-care, and ensure time for personal and family life ",
                "Prioritize work but find ways to integrate personal and family time ",
                "Overcommit to work responsibilities and neglect personal and family life",
                "Feel uncertain about balancing work and personal responsibilities"
            ],
            'Correct5': "Set clear boundaries, prioritize self-care, and ensure time for personal and family life",
            'Correct3': "Prioritize work but find ways to integrate personal and family time"
        },
        {
            'QID': 'MHQ057',
            'Question': "How do you adapt to changes in your social circles and make new connections?",
            'Options': [
                "Embrace change, actively seek new connections, and engage in social activities ",
                "Maintain existing social circles but occasionally make new connections ",
                "Resist changes in social circles and prefer stability",
                "Feel uncertain about adapting to social changes and making new connections"
            ],
            'Correct5': "Embrace change, actively seek new connections, and engage in social activities",
            'Correct3': "Maintain existing social circles but occasionally make new connections"
        },
        {
            'QID': 'MHQ058',
            'Question': "When planning for retirement, what's your approach to financial preparation?",
            'Options': [
                "Develop a detailed retirement plan, set savings goals, and invest strategically ",
                "Have a general idea of retirement goals but lack a specific financial plan ",
                "Avoid actively planning for retirement and hope for the best",
                "Feel uncertain about effective retirement planning"
            ],
            'Correct5': "Develop a detailed retirement plan, set savings goals, and invest strategically",
            'Correct3': "Have a general idea of retirement goals but lack a specific financial plan"
        },
        {
            'QID': 'MHQ059',
            'Question': "How do you cope with the aging process and changes in physical well-being?",
            'Options': [
                "Prioritize health through regular exercise, healthy eating, and medical check-ups ",
                "Acknowledge changes but sometimes struggle with adapting to them ",
                "Neglect health concerns and avoid addressing age-related changes",
                "Feel uncertain about effectively managing physical well-being in the aging process"
            ],
            'Correct5': "Prioritize health through regular exercise, healthy eating, and medical check-ups",
            'Correct3': "Acknowledge changes but sometimes struggle with adapting to them"
        },
        {
            'QID': 'MHQ060',
            'Question': "How do you approach finding fulfillment and purpose in your life as you age?",
            'Options': [
                "Reflect on personal values, set meaningful goals, and actively pursue purpose ",
                "Have general ideas of what brings fulfillment but lack a clear plan ",
                "Avoid actively seeking purpose, feeling content with the present",
                "Feel uncertain about how to find fulfillment and purpose in your current stage of life"
            ],
            'Correct5': "Reflect on personal values, set meaningful goals, and actively pursue purpose",
            'Correct3': "Have general ideas of what brings fulfillment but lack a clear plan"
        },
        {
            'QID': 'MHQ061',
            'Question': "How do you approach self-reflection and personal growth in your current stage of life?",
            'Options': [
                "Regularly engage in self-reflection, set personal growth goals, and pursue continuous improvement ",
                "Occasionally reflect on personal growth but without a structured plan ",
                "Avoid self-reflection and personal development activities",
                "Feel uncertain about how to approach self-reflection and personal growth"
            ],
            'Correct5': "Regularly engage in self-reflection, set personal growth goals, and pursue continuous improvement",
            'Correct3': "Occasionally reflect on personal growth but without a structured plan"
        },
        {
            'QID': 'MHQ062',
            'Question': "When facing major life transitions, such as parenthood or career changes, how do you adapt?",
            'Options': [
                "Embrace change, plan for transitions, and seek support from others ",
                "Navigate transitions but sometimes feel the impact on your well-being ",
                "Struggle to adapt to major life changes and feel overwhelmed",
                "Feel uncertain about effectively managing major life transitions"
            ],
            'Correct5': "Embrace change, plan for transitions, and seek support from others",
            'Correct3': "Navigate transitions but sometimes feel the impact on your well-being"
        },
        {
            'QID': 'MHQ063',
            'Question': "How do you maintain a sense of community and social connections as you age?",
            'Options': [
                "Actively engage in community activities, maintain friendships, and foster social connections ",
                "Keep existing social connections but may not actively seek new ones ",
                "Withdraw from social activities and prefer solitude",
                "Feel uncertain about fostering community and social connections"
            ],
            'Correct5': "Actively engage in community activities, maintain friendships, and foster social connections",
            'Correct3': "Keep existing social connections but may not actively seek new ones"
        },
        {
            'QID': 'MHQ064',
            'Question': "When it comes to technology and digital communication, how do you stay informed and connected?",
            'Options': [
                "Embrace technology, stay updated on digital trends, and use it to connect with others ",
                "Use technology but may feel overwhelmed by constant changes ",
                "Avoid using technology for communication and information",
                "Feel uncertain about navigating technology in your current stage of life"
            ],
            'Correct5': "Embrace technology, stay updated on digital trends, and use it to connect with others",
            'Correct3': "Use technology but may feel overwhelmed by constant changes"
        },
        {
            'QID': 'MHQ065',
            'Question': "How do you prioritize and maintain a healthy lifestyle, including diet and exercise?",
            'Options': [
                "Prioritize health with regular exercise, balanced diet, and preventive health measures ",
                "Maintain a healthy lifestyle but may occasionally struggle to stay consistent ",
                "Neglect health habits and don't actively pursue a healthy lifestyle",
                "Feel uncertain about effectively prioritizing and maintaining a healthy lifestyle"
            ],
            'Correct5': "Prioritize health with regular exercise, balanced diet, and preventive health measures",
            'Correct3': "Maintain a healthy lifestyle but may occasionally struggle to stay consistent"
        },
        {
            'QID': 'MHQ066',
            'Question': "How do you manage and balance diverse responsibilities, including family, work, and personal pursuits?",
            'Options': [
                "Prioritize tasks, set clear boundaries, and balance responsibilities effectively ",
                "Manage responsibilities but sometimes feel overwhelmed by competing demands ",
                "Struggle to balance responsibilities and often feel stressed",
                "Feel uncertain about effectively managing diverse responsibilities"
            ],
            'Correct5': "Prioritize tasks, set clear boundaries, and balance responsibilities effectively",
            'Correct3': "Manage responsibilities but sometimes feel overwhelmed by competing demands"
        },
        {
            'QID': 'MHQ067',
            'Question': "How do you cope with the loss of loved ones and navigate the grieving process?",
            'Options': [
                "Seek support from others, engage in the grieving process, and honor the memories ",
                "Grieve in your own way but may find it challenging to cope with loss ",
                "Avoid confronting grief and loss, pushing emotions aside",
                "Feel uncertain about navigating the grieving process effectively"
            ],
            'Correct5': "Seek support from others, engage in the grieving process, and honor the memories",
            'Correct3': "Grieve in your own way but may find it challenging to cope with loss"
        },
        {
            'QID': 'MHQ068',
            'Question': "How do you approach financial planning for your children's education or other future expenses?",
            'Options': [
                "Develop a comprehensive financial plan, set savings goals, and invest strategically ",
                "Have general financial goals for future expenses but lack a specific plan ",
                "Avoid actively planning for future expenses and hope for the best",
                "Feel uncertain about effective financial planning for future expenses"
            ],
            'Correct5': "Develop a comprehensive financial plan, set savings goals, and invest strategically",
            'Correct3': "Have general financial goals for future expenses but lack a specific plan"
        },
        {
            'QID': 'MHQ069',
            'Question': "How do you maintain a sense of purpose and fulfillment in your career as you progress in your professional life?",
            'Options': [
                "Set meaningful career goals, adapt to changes, and actively seek fulfillment ",
                "Find satisfaction in your career but may occasionally feel a lack of purpose ",
                "Feel stuck in your career and uncertain about finding purpose",
                "Feel uncertain about how to navigate career fulfillment as you age"
            ],
            'Correct5': "Set meaningful career goals, adapt to changes, and actively seek fulfillment",
            'Correct3': "Find satisfaction in your career but may occasionally feel a lack of purpose"
        },
        {
            'QID': 'MHQ070',
            'Question': "How do you approach making time for personal hobbies and interests amid a busy schedule?",
            'Options': [
                "Prioritize personal interests, allocate time for hobbies, and find joy in leisure activities ",
                "Engage in hobbies but struggle to consistently make time for personal interests ",
                "Neglect personal interests due to a busy schedule",
                "Feel uncertain about effectively making time for personal hobbies"
            ],
            'Correct5': "Prioritize personal interests, allocate time for hobbies, and find joy in leisure activities",
            'Correct3': "Engage in hobbies but struggle to consistently make time for personal interests"
        }
    ]
    def get(self,request):
        cat = int(request.GET.get('cat',0))
        if cat:
            if cat == 1:
                context = {
                    'quizData': self.questions_cat1
                }
            elif cat == 2:
                context = {
                    'quizData': self.questions_cat2
                }
            elif cat == 3:
                context = {
                    'quizData': self.questions_cat1
                }
            return render(request,'dashboard/mental_health_c.html',context)
        return render(request,"dashboard/mental_health_sel.html")