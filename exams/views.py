import json
from openai import AzureOpenAI
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.utils import timezone
from django.conf import settings
from django.views.decorators.http import require_POST
from .models import ExamSet, Section, Question, ExamAttempt, StudentResponse


ARTICLES = {
    'ideal-worker': {
        'title': "Why the idea of an 'ideal worker' can be so harmful for people with mental health conditions",
        'author': 'Hadar Elraz',
        'author_initial': 'H',
        'date': '3 February 2026',
        'source': 'The Conversation',
        'tags': ['Workplace', 'Mental Health', 'Stigma'],
        'content': """
<p>In the modern world of work, the &ldquo;ideal worker&rdquo; is a dominant yet dangerous concept that can dictate workplace norms and expectations. This archetype describes an employee who is boundlessly productive, constantly available and emotionally stable at all times.</p>

<p>What makes this trope so flawed is that it assumes workers have no caring responsibilities outside work, or have unrealistic physical and psychological capabilities. It&rsquo;s intended to drive efficiency, but in fact it is a standard that very few people can reach. It marginalises people who deviate from these rigid standards, including workers managing mental health conditions.</p>

<p>We are researchers in management and health, and our recent paper found that this &ldquo;ideal worker&rdquo; is a means of creating stigma. This stigma is embedded in processes and policies, creating a yardstick against which all employees are measured.</p>

<p>The study is based on in-depth interviews with a diverse group of employees with mental health conditions (including depression, bipolar disorder, anxiety and OCD). They worked across the private, public and third sectors in various jobs, including accounting, engineering, teaching and senior management.</p>

<p>For workers with mental health conditions, the expectation of emotional steadiness creates a conflict with the often fluctuating nature of their conditions.</p>

<p>When organisations are seen to value the ideal worker archetype, they can end up creating barriers to meaningful inclusion. In our paper we understand these as both &ldquo;barriers to doing&rdquo; and &ldquo;barriers to being&rdquo;.</p>

<p>What this means is that workplaces end up with rigid workloads and inflexible expectations (&ldquo;barriers to doing&rdquo;). As such, they fail to accommodate people with invisible or fluctuating symptoms. They can also undermine a worker&rsquo;s identity and self-worth (&ldquo;barriers to being&rdquo;), framing them as unreliable or incompetent simply because they do not meet the standards of the ideal worker.</p>

<p>Because employees with mental health conditions often fear being perceived as weak, a burden or fragile, they frequently work excessively hard to prove their value. This means that these employees might compromise their resting and unwinding time in order to live up to workplace expectations.</p>

<p>But of course, these efforts create strain at the personal level. These workers can end up putting themselves at greater risk of relapse or ill health. Our research found that overworking to mask mental health symptoms (working unpaid hours to make up for times when they are unwell, for example) can suggest an organisational culture that may not be inclusive enough.</p>

<h2>What&rsquo;s really happening</h2>

<p>HR practices may assume that mental health conditions should be managed by employees alone, rather than with support from the organisation. At the same time, this constant pressure to over-perform can exacerbate mental health conditions, leading to a vicious cycle of stress, exhaustion and even more stigma.</p>

<p>The ideal worker norm forces many employees into keeping their mental health conditions to themselves. They may see hiding their struggles as a tactical way of protecting their professional identity.</p>

<p>In an environment that rewards constant productivity, disclosing a condition that might require reasonable adjustments could be seen as a professional risk. In other words, stigma may compromise career chances.</p>

<p>Participants in our research reported lying on health questionnaires or hiding symptoms because the climate in their workplace signalled that mental health conditions were poorly understood. But this secrecy creates a massive emotional burden, as workers felt pressure to constantly monitor their health, mask their condition and schedule medical appointments in secret.</p>

<p>Paradoxically, while this approach allows people to remain employed, it reinforces the structures that demand their silence. And it ensures that workplace support remains invisible or inaccessible.</p>

<p>Our analysis showed a stark contrast between perceptions of support for people with physical impairments and that for employees with mental health conditions. While physical aids like ramps are often visible and accepted, workers setting out their mental health needs frequently faced the risk of stigma, ignorance or disbelief.</p>

<p>By holding on to the ideal worker archetype, organisations are not only failing to fulfil their duty of care. They may also be undermining their own long-term sustainability if they lose skilled labour. Then there are the costs of constant recruitment and retraining.</p>

<p>Managing stigma is a workplace burden that can lead to burnout or divert energy away from a worker&rsquo;s core tasks. We suggest a fundamental shift for employers: moving away from chasing the &ldquo;ideal worker&rdquo; towards creating &ldquo;ideal workplaces&rdquo; instead. This means challenging the assumption that productivity must be uninterrupted and that emotional stability is a prerequisite for professional value.</p>

<p>It also means focusing on the quality of an employee&rsquo;s contribution rather than judging their constant availability or productivity. And it means designing work environments from the ground up to support diverse needs, so that mental health conditions are normalised. This would reduce the need for employees to keep conditions secret.</p>

<p>Ultimately, the problem with the ideal worker archetype is that it is a persistent myth that ignores the reality of human diversity. True equity requires organisations to stop trying to shape individuals to fit the mould and instead rethink work norms to support all employees so that everyone can play a part in enhancing the business.</p>
"""
    },
    'table-tennis': {
        'title': 'A brief history of table tennis in film \u2013 from Forrest Gump to Marty Supreme',
        'author': 'Jeff Scheible',
        'author_initial': 'J',
        'date': '3 February 2026',
        'source': 'The Conversation',
        'tags': ['Film', 'Sports', 'Culture'],
        'content': """
<p>Table tennis and film have a surprisingly entangled history. Both depended on the invention of celluloid &ndash; which not only became the substrate of film, but is also used to make ping pong balls.</p>

<p>Following a brief ping pong craze in 1902, the game largely disappeared and was widely assumed to have been a passing fad. More than 20 years later, however, the British socialite, communist spy and filmmaker Ivor Montagu went to great lengths to establish the game as a sport &ndash; a story I explore in my current book project on ping pong and the moving image.</p>

<p>He founded the International Table Tennis Federation (ITTF) and codified the rules of the game in both a book and a corresponding short film, <em>Table Tennis Today</em> (1929).</p>

<p>Montagu presided over the ITTF for several decades. In 1925, the same year he founded the ITTF, Montagu also co-founded the London Film Society. The society helped introduce western audiences to experimental and art films that are now considered classics.</p>

<p>The game of table tennis has subsequently appeared at a number of moments when filmmakers and artists were experimenting with new technologies. An early example appears in one of the first works of &ldquo;visual music&rdquo;: <em>Rhythm in Light</em> (1934) by Mary Ellen Bute.</p>

<p>Meanwhile, an early work of expanded cinema, <em>Ping Pong</em> (1968) by the artist Valie Export, invited audiences to pick up a paddle and ball and attempt to strike a physical ball against the representation of one moving on the cinema screen. Atari&rsquo;s adaptation of the game into the interactive <em>Pong</em> (1972) is often considered the first video game.</p>

<p>Perhaps the most familiar cinematic example of all, however, is the digital simulation of a photorealistic ping pong ball &ndash; made possible by a then-new regime of computer-generated imagery. It helped Tom Hanks appear to be a ping pong whiz in the Academy-Award-winning <em>Forrest Gump</em> (1994).</p>

<p>There are a number of other fascinating moments in which the game surfaces meaningfully: in Powell and Pressburger&rsquo;s <em>A Matter of Life and Death</em> (1946), Jacques Tati&rsquo;s <em>M Hulot&rsquo;s Holiday</em> (1953), Michael Haneke&rsquo;s <em>71 Fragments of a Chronology of Chance</em> (1994), and Agnes Varda and JR&rsquo;s <em>Faces Places</em> (2017).</p>

<p>And every day for more than two years, from 2020 to 2022, one of the world&rsquo;s most beloved filmmakers, David Lynch, uploaded YouTube videos in which he pulled a numbered ping pong ball from a jar and declared it &ldquo;today&rsquo;s number&rdquo;. It was a fittingly Dada-esque gesture that stands among the last mysterious works he shared with the world.</p>

<p>Enter Josh Safdie&rsquo;s <em>Marty Supreme</em>. The title sequence alone discovers a new way of visualising the game&rsquo;s iconography, as we see a sperm fertilise an egg, which then transforms into a ping pong ball (the digital effects first witnessed in <em>Gump</em> are now fully integrated into popular cinema).</p>

<h2>Why Marty Supreme is different</h2>

<p><em>Marty Supreme</em> is very loosely based on the real-life player Marty Reisman (here Marty Mauser, played by Timoth&eacute;e Chalamet). What sets it apart from earlier cinematic appearances of table tennis is that it centres the game as a sport.</p>

<p>When table tennis has previously appeared in film, it is usually to help show off new special effects or as a brief plot device. Or it frequently appears in the background, helping to furnish the mise-en-scene of an office, basement, or bar. In these instances, we might not notice the game or its materials at all. When it does have a narrative function, it usually occupies a single scene, frequently serving to stage or resolve fraught interpersonal relations between the characters who are playing.</p>

<p>In <em>Marty Supreme</em>, however, table tennis seems neither tethered to special effects nor, certainly, to the game&rsquo;s &ldquo;background&rdquo; status. Chalamet trained extensively over the seven years he spent preparing for the role, even taking his own table to the desert while filming <em>Dune</em> (2021). And despite the film&rsquo;s sometimes compelling eccentricities, <em>Marty Supreme</em> in many senses follows the generic blueprint of a sports film.</p>

<p>Safdie has made a sports film, coincidentally or not, like his frequent collaborator and brother Benny Safdie, whose wrestling film <em>The Smashing Machine</em> was also released this past year. <em>Marty Supreme</em>, though, revolves around an athlete who plays a game that generally has been assumed to not have enough gravitas to command a place in the genre or to hold an audience&rsquo;s interest.</p>

<p>The absence of sports films about ping pong certainly speaks to ways in which it is perceived as something not worth taking too seriously, for reasons that are surely at least partially linked to the same reasons for which the game is often celebrated. It is perceived to be what I refer to as an &ldquo;equalising&rdquo; sport, open to people and bodies of all backgrounds and types.</p>

<p>As actor Susan Sarandon, who founded her own chain of ping pong bars, puts it: &ldquo;Ping pong cuts across all body types and gender &ndash; everything, really &ndash; because little girls can beat big muscley guys. You don&rsquo;t get hurt; it is not expensive; it is really good for your mind. It is one of the few sports that you can play until you die.&rdquo;</p>

<p>This perception of the game has perhaps also led it to appear in more comedic contexts, with athletes embodied by actors we might more readily laugh at, as source material for visual and sonic gags, from a slapstick scene in <em>You Can&rsquo;t Cheat an Honest Man</em> (1939) to the widely panned <em>Balls of Fury</em> (2007).</p>

<p>The tension between the game&rsquo;s perceived triviality and Mauser&rsquo;s extreme dedication lends <em>Marty Supreme</em> a vast blank canvas &ndash; or ping pong table &ndash; onto which its oscillations can be painted, or played&hellip; and in turn felt by the audience, with its high highs and low lows.</p>

<p>While it&rsquo;s great that a talented director has poured his heart into a cinematic treatment of Reisman for the screen, I&rsquo;m holding out hope for an Ivor Montagu film, which could be even more beholden to its real-life character &ndash; and even more wild.</p>
"""
    },
    'covert-filming': {
        'title': 'Is it illegal to make online videos of someone without their consent? The law on covert filming',
        'author': 'Subhajit Basu',
        'author_initial': 'S',
        'date': '3 February 2026',
        'source': 'The Conversation',
        'tags': ['Law', 'Privacy', 'Technology'],
        'content': """
<p>Imagine a stranger starts chatting with you on a train platform or in a shop. The exchange feels ordinary. Later, it appears online, edited as &ldquo;dating advice&rdquo; and framed to invite sexualised commentary. Your face, and an interaction you didn&rsquo;t know was being recorded, is pushed into feeds where strangers can identify, contact and harass you.</p>

<p>This is a reality for many people, though the most shocking examples are mainly affecting women. A BBC investigation recently found that men based outside of the UK have been profiting from covertly filming women on nights out in London and Manchester and posting the videos on social media.</p>

<p>In the UK, filming someone in public &ndash; even covertly &ndash; is not automatically unlawful. Sometimes, it is socially valuable (think of people recording violence or police misconduct).</p>

<p>But once a person is identifiable and the clip is uploaded for views or profit, it can become unlawful under data protection law and, in more intrusive cases, privacy or harassment law. The problem here is what the filming is for, how it is done and what the platforms do with it.</p>

<p>UK law is cautious about a general claim to &ldquo;privacy in public&rdquo;. There is a key distinction in case law between being seen in a public place and being recorded for redistribution.</p>

<p>Courts have accepted that privacy can apply even in public, depending on circumstances. In the case of <em>Campbell v MGN</em> (2004), the House of Lords ruled that the Daily Mirror had breached model Naomi Campbell&rsquo;s privacy by publishing photos that, while taken in public, exposed her private medical information.</p>

<p>The rise of smartphones and now wearable cameras has made covert capture cheaper, more discreet and more accessible. With smart glasses, recording can look like eye contact.</p>

<p>Capture is frictionless: the file is ready to upload before the person filmed even knows it exists. And manufacturer safeguards such as recording lights are already reportedly being bypassed by users.</p>

<p>Once it&rsquo;s been uploaded, modern social media platforms allow this content to become easily scalable, searchable and profitable.</p>

<p>Context is what shifts the stakes. Covert filming, an intrusive focus on the body and publication at scale can turn an everyday moment into exposure that invites harassment.</p>

<h2>Privacy in public</h2>

<p>Public life has always involved being seen. The harm is being made findable and targetable, at scale. This is why the most practical legal tool is data protection. Under the UK General Data Protection Regulation (GDPR), when people are identifiable in a video, recording and uploading it is considered processing of personal data.</p>

<p>The uploader and platform must therefore comply with GDPR rules, which in this case would (usually) mean not posting identifiable footage of a stranger in the first place or, removing the details that identify them and taking the clip down quickly if the person objects.</p>

<p>UK GDPR does not apply to purely personal or household activity, with no professional or commercial connection. This is a narrow exemption &ndash; &ldquo;pickup artist&rdquo; channels and monetised social media posts are unlikely to fall within it.</p>

<p>Harassment law may apply where the filming and posting is followed by repeated contact, threats or encouraging others to target the person filmed, which causes them alarm or distress.</p>

<h2>Lagging enforcement</h2>

<p>Harm spreads faster than the law can respond. A clip can be uploaded, shared and monetised within seconds. Enforcement of privacy and data protection law is split between the Information Commissioner&rsquo;s Office, Ofcom, police and courts.</p>

<p>Victims are left to rely on platform reporting tools, and duplicates often continue to spread even after posts are taken down. Arguably, prevention would be more effective than after-the-fact removal.</p>

<p>The temptation is to call for a new offence of &ldquo;filming in public&rdquo;. In my view, this risks being either too broad (chilling legitimate recording) or too narrow (missing the combination of factors &ndash; covert filming, identifiability, platform amplification and monetisation that make this a problem).</p>

<p>A better approach would be twofold. First, treating wearable recording devices as higher-risk consumer tech, and requiring safeguards that work in practice. For example: conspicuous, genuinely tamper-resistant recording indicators; privacy-by-default settings; and audit logs so misuse is traceable. The law could build in clear public-interest exemptions (journalism, documenting wrongdoing) so rules do not become a backdoor ban on recording.</p>

<p>There are precedents for regulating consumer tech in this way. For example, the UK has strict security requirements for connectable devices like smart TVs to prevent cyberattacks.</p>

<p>Second, platforms need a clear requirement to reduce the harm caused by covert filming. In practice, that means spotting and obscuring identifiers such as phone numbers and workplace details, warning users when a stranger is identifiable, fast-tracking complaints from the person filmed, blocking re-uploads, and removing monetisation from this content.</p>

<p>The Online Safety Act provides a framework for addressing this problem, but it is not a neat checklist for prevention. Where it clearly applies is when the content itself, or the response it triggers, amounts to illegal harassment or stalking. Those are priority offences in the act, so platforms are expected to assess and mitigate those risks.</p>

<p>The awkward truth is that some covert, degrading clips may be harmful without being obviously illegal at the point of upload, until threats, doxxing or stalking follow.</p>

<p>Privacy in public will not be protected by slogans or a tiny recording light. It will be protected when existing legal principles are applied robustly. And when enforcement is designed for the speed, incentives and business models that shape what people see and share online.</p>
"""
    },
    'house-burping': {
        'title': 'House burping: what is this German habit and is it good for your health?',
        'author': 'Vikram Niranjan',
        'author_initial': 'V',
        'date': '5 February 2026',
        'source': 'The Conversation',
        'tags': ['Health', 'Environment', 'Lifestyle'],
        'content': """
<p>&ldquo;House burping&rdquo; is the latest thing cluttering people&rsquo;s feeds: short clips of people flinging open every window and door, announcing they&rsquo;re &ldquo;burping&rdquo; their home to get rid of stale, germ-filled air. Behind the playful name is a serious question: does this actually make a home healthier, or are people just swapping indoor germs for outdoor pollution?</p>

<p>In Germany, this trend looks less like a revolution and more like everyday life. <em>L&uuml;ften</em> &ndash; literally &ldquo;airing out&rdquo; &ndash; and <em>Sto&szlig;l&uuml;ften</em>, or &ldquo;shock ventilation&rdquo;, have long involved opening windows wide for a few minutes to let fresh air race through, even in the depths of winter. Some German rental contracts even mention regular airing as part of looking after the property, mainly to prevent damp and mould.</p>

<p>The health logic is simple. Indoor air collects moisture from showers and cooking, smoke and particles from stoves and candles, chemicals from cleaning sprays and furniture, and tiny particles and viruses that people breathe out.</p>

<p>In a previous study my colleagues and I conducted, we found many diseases linked to indoor air pollution. Over time, these build up, especially in well-insulated homes that keep heat &ndash; and pollution &ndash; in. When the house is &ldquo;burped&rdquo;, the sudden rush of outdoor air dilutes this mixture and pushes a good chunk of it outside.</p>

<p>This is particularly important for infections that spread through the air. During the COVID pandemic, public health agencies stressed that better ventilation &ndash; including simply opening windows &ndash; could help cut the risk of catching the virus indoors. In one classroom study, opening all windows and doors dropped carbon dioxide levels by about 60% and reduced a simulated &ldquo;viral load&rdquo; by more than 97% over an eight-hour day, shrinking the area with higher infection risk to around 15% of the room.</p>

<p>Pets breathe the same air and can act as early warning signs of trouble. Veterinary studies link poor indoor air to lung irritation in dogs and cats, especially near the floor where particles settle &ndash; a reminder that stale air harms the whole household.</p>

<p>But the air outside is not always clean. Tiny particles from traffic and factories, and gases such as nitrogen dioxide, damage the heart, lungs and brain and are now recognised as major causes of illness and early death. In many cities, most of the fine particles inside homes and schools actually come from outside and seep in through gaps, vents and, of course, open windows.</p>

<p>Where you live shapes that trade-off. Homes close to busy main roads or motorways tend to have higher levels of traffic-related particles and nitrogen dioxide indoors, especially when windows facing the road are opened.</p>

<p>That means flinging open roadside windows at rush hour may bring in a surge of exhaust, tyre and brake dust just as traffic pollution peaks. For people with asthma, heart disease or chronic lung problems, that extra pollution can undo some of the health benefits of better ventilation.</p>

<h2>The right time to burp</h2>

<p>Timing also matters. In many cities, outdoor pollution is highest during the morning and evening commute and lower late at night or in the middle of the day. Short bursts of house burping outside these peaks &ndash; or just after rain, which can temporarily wash some particles from the air &ndash; may offer a better balance between infection control and pollution exposure.</p>

<p>Poor indoor air does not stop at the lungs. Studies link higher levels of fine particles and carbon dioxide to poorer concentration, slower thinking and raised risks of anxiety and depression. A stuffy home quietly chips away at mood and mental sharpness for everyone inside.</p>

<p>How the burp is done makes a difference to comfort and energy bills. German-style <em>Sto&szlig;l&uuml;ften</em>, where all windows are opened fully for a short time, rapidly exchanges air but does not cool walls and furniture as much as leaving a small window open all day. Cross-ventilation &ndash; opening windows on opposite sides of the home &ndash; usually shifts air faster.</p>

<p>For most households, a practical middle ground is possible. House burping is more likely to be helpful when it is done in short bursts, away from busy traffic times, and on the sides of the home that face quieter streets or greener spaces.</p>

<p>So the social media trend has a point, even if the name raises a smile. A home that never burps is likely to have higher levels of indoor pollution and a greater build-up of exhaled air, especially during virus season. Give your home a mini spa break at the right time: throw open the windows, let it burp out the stale air, and invite a burst of fresh stuff in. Your lungs, brain and pets will thank you.</p>
"""
    },
    'forever-chemicals': {
        'title': "How the UK government plans to limit 'forever chemical' pollution \u2013 and what's missing",
        'author': 'Ivan Kourtchev',
        'author_initial': 'I',
        'date': '5 February 2026',
        'source': 'The Conversation',
        'tags': ['Environment', 'Science', 'Policy'],
        'content': """
<p>The UK government has published its first national plan to deal with per- and polyfluoroalkyl substances, better known as PFAS or &ldquo;forever chemicals&rdquo;. These chemicals have been used for decades in products such as firefighting foams, non-stick cookware, clothing, electronics and many industrial processes. Because many PFAS do not break down easily, they are now widely detected in the environment and in human blood and tissues.</p>

<p>The policy document, <em>PFAS Plan: Building a Safer Future Together</em>, follows growing public concern, media investigations and years of pressure from scientists calling for stronger controls. This marks an important moment for UK chemicals policy. The plan represents a step forward, but it avoids many of the hardest regulatory choices associated with PFAS.</p>

<p>Unlike many pollutants, PFAS are not a single substance. There are several thousand PFAS in use or in circulation, each with different properties and behaviours. Some have been linked to health effects, such as liver toxicity, developmental problems and negative effects on the immune system. For many others, evidence remains sparse or uncertain.</p>

<p>PFAS are also highly mobile. They can be transported through air, deposited onto land or water, and then re-enter the atmosphere or food chain. Contamination measured in one location may originate from industrial activity, waste handling, consumer products or historic uses far away.</p>

<p>In the UK, regulation has so far focused on a small number of well-studied PFAS, mainly through drinking water standards. This has left the wider group of PFAS, and their long-term accumulation in air and soil, largely outside the scope of formal regulation.</p>

<p>The new PFAS plan is intended to provide that framework. Rather than introducing sweeping new bans, it sets out how PFAS risks should be assessed and managed over time, with a strong emphasis on coordination across government, regulators, researchers and industry.</p>

<p>A central element of the plan is its focus on evidence. It recognises that PFAS pollution is not limited to water and soil, but also includes air emissions from manufacturing, industrial processes and waste treatment.</p>

<h2>A starting point</h2>

<p>At the same time, the new plan leaves many hard decisions for later. It does not ban PFAS as a class, set timelines for phase-outs or define which uses should ultimately be considered essential. Much depends on future consultations and how quickly new evidence emerges.</p>

<p>This caution has attracted criticism, but it reflects a real constraint. New PFAS continue to enter the market, sometimes as replacements for substances that have already been restricted. Regulating a group of chemicals that continues to evolve is inherently difficult, particularly when emissions are diffuse and exposure pathways complex.</p>

<p>In July 2025, the EU adopted a new Chemicals Industry Action Plan to support a transition away from PFAS through measures such as innovation, substitution, and improved data generation.</p>

<p>Taken together, the UK&rsquo;s PFAS plan is best seen as a starting point rather than a solution. It brings air, water and land into a single policy debate and recognises that PFAS pose a long-term challenge rather than a short-term compliance issue.</p>

<p>Whether it leads to meaningful reductions in exposure will depend on what follows: how quickly methods capable of addressing the many thousands of PFAS in commerce and the environment are developed and validated; how monitoring data is used; and whether future decisions prevent new PFAS problems from emerging.</p>
"""
    },
    'city-skylines': {
        'title': 'City skylines need an upgrade in the face of climate stress',
        'author': 'Mohamed Shaheen',
        'author_initial': 'M',
        'date': '4 February 2026',
        'source': 'The Conversation',
        'tags': ['Climate', 'Engineering', 'Cities'],
        'content': """
<p>When structural engineers design a building, they aren&rsquo;t just stacking floors; they are calculating how to win a complex battle against nature. Every building is built to withstand a specific &ldquo;budget&rdquo; of environmental stress &ndash; the weight of record snowfalls, the push of powerful winds and the expansion caused by summer heat.</p>

<p>To do this, engineers use hazard maps and safety codes. These are essentially rulebooks based on decades of historical weather data. They include safety margins to ensure that even if a small part of a building fails, the entire structure won&rsquo;t come crashing down like a house of cards.</p>

<p>The problem is that these rulebooks are becoming obsolete. Most of our iconic high-rises were built in the 1970s and 80s &ndash; a world that was cooler, with more predictable tides and less violent storms. Today, that world no longer exists.</p>

<p>Climate change acts as a threat multiplier, making the consequences of environmental stress on buildings much worse. It rarely knocks a building down on its own. Instead, it finds the tiny cracks, rusting support beams and ageing foundations and pushes them toward a breaking point.</p>

<p>The 2021 collapse of Champlain Towers South in Miami, Florida, killed 98 people. While the 12-storey building had original design issues, decades of rising sea levels and salty coastal air acted as a catalyst, allowing saltwater to seep into the basement and garage.</p>

<p>When salt reaches the steel rods inside concrete that provide structural strength, the metal rusts and expands. This creates massive internal pressure that cracks the concrete from the inside out &mdash; a process engineers call spalling.</p>

<p>In Hong Kong during Super Typhoon Mangkhut in 2018, wind speeds hit a terrifying 180 miles per hour. When strong winds hit a wall of skyscrapers, they squeeze between the buildings and speed up. This pressure turned hundreds of offices into wind tunnels, causing glass windows to pop out of their frames.</p>

<p>In the US, a study of 370 million property records from 1945 to 2015 found over half of all structures are in hazard hotspots. In the UK, climate-driven weather claims hit &pound;573 million in 2023, a 36% rise from 2022.</p>

<h2>Maintenance is our best defence</h2>

<p>Much of the world&rsquo;s building stock is therefore entering its middle age under environmental conditions it was never designed to face. Instead of panicking or tearing everything down, the solution is to adapt and treat building maintenance as a form of climate resilience &ndash; not as an optional extra.</p>

<p>Mid-life building upgrades can help protect our skylines for the next 50 years. Our hazard maps must look at future climate models &mdash; not just historical weather &mdash; to set new safety standards.</p>

<p>Climate change isn&rsquo;t rewriting the laws of engineering, but it is rapidly eating away at our margins of safety. If we want our cities to remain standing, we must act now &ndash; before small, invisible stresses accumulate into irreversible failure.</p>
"""
    },
    'bamboo-superfood': {
        'title': "Bamboo: superfood or superfad? Here's what our study actually said",
        'author': 'Lee Smith',
        'author_initial': 'L',
        'date': '4 February 2026',
        'source': 'The Conversation',
        'tags': ['Food', 'Health', 'Science'],
        'content': """
<p>According to the New York Post, our research team has discovered a much-overlooked &ldquo;superfood&rdquo;: bamboo shoots. Before you rush out to harvest the ornamental bamboo growing in your garden, there are a few things you should know.</p>

<p>We systematically reviewed all the available evidence on bamboo as a food and its effect on human health. The research base turned out to be surprisingly thin &ndash; just 16 studies met our criteria, including four trials in people and four that used cells in a dish.</p>

<p>There is evidence of some positive health effects from eating bamboo. One study showed that eating bamboo shoots in cookies better controlled blood sugar levels, and that more bamboo consumption translated to further lowered levels.</p>

<p>Other studies documented the beneficial effects of the fibre they contain. This isn&rsquo;t limited to the inevitable bowel movements but also includes the delightfully termed &ldquo;faecal volume&rdquo;, both of which were shown to improve.</p>

<p>Also, compared to a fibre-free diet, bamboo shoots lowered overall cholesterol and LDL cholesterol (so-called &ldquo;bad cholesterol&rdquo;) that can build up in blood vessels and cause heart disease.</p>

<p>One unusual benefit of bamboo is that it contains flavonoids &ndash; plant compounds that can protect against acrylamide, a potentially harmful chemical that forms when starchy foods are cooked at high temperatures.</p>

<p>Eating bamboo may also help calm inflammation and protect cells from damage. In lab tests, it reduced immune cell activity by 63% and halved the release of substances that trigger inflammation in the body.</p>

<h2>The grass isn&rsquo;t all green, though</h2>

<p>However, if bamboo isn&rsquo;t properly prepared, it can lead to problems. One study linked it to an increased risk of a condition called goitre. Poorly prepared bamboo contains chemicals called cyanogenic glycosides, which the body converts into another chemical called thiocyanate. These block the thyroid from using iodine effectively.</p>

<p>Some of the bamboo samples analysed contained heavy metals, like arsenic, cadmium and lead. While most were measured well within permitted limits, lead was found in amounts up to 4.6 times the permitted levels in 21 of the samples assessed.</p>

<p>The evidence base in this area isn&rsquo;t as strong as it could be. The few relevant studies we did find had some methodological issues.</p>

<p>Still, the research shows that bamboo shoots have potential as a sustainable, healthy food. And like the shoots themselves, interest in this area is only likely to grow &ndash; rapidly.</p>
"""
    },
    'alzheimers-test': {
        'title': "How our lab is helping develop an Alzheimer's test that can be done at home",
        'author': 'Eleftheria Kodosaki',
        'author_initial': 'E',
        'date': '4 February 2026',
        'source': 'The Conversation',
        'tags': ['Medicine', 'Science', 'Technology'],
        'content': """
<p>Imagine diagnosing one of the most challenging neurological diseases with just a quick finger-prick, a few drops of blood and a test sent in the post. This may sound like science fiction, but we are hoping our research could soon help it become a reality.</p>

<p>Our team at the UK Dementia Research Institute&rsquo;s Biomarker Factory at UCL are part of the global effort working to develop and validate a test for Alzheimer&rsquo;s disease.</p>

<h2>What do finger-prick tests look for?</h2>

<p>At their core, these finger-prick tests are designed to detect specific biomarkers. Biomarkers are biological molecules found in the blood which indicate signs of disease. In the case of Alzheimer&rsquo;s disease, the brain gradually accumulates abnormal proteins. These proteins form structures such as amyloid plaques and tau tangles which damage the brain&rsquo;s neural networks.</p>

<p>These abnormal proteins can be detected in the brain, cerebrospinal fluid and, importantly, the blood years before symptoms arise.</p>

<p>Recently, research has also shown these biomarkers can be measured in dried blood samples from a simple finger-prick. A study focusing on 337 people showed that these dried blood samples can reliably detect Alzheimer&rsquo;s-related changes in biomarkers with a diagnostic accuracy of around 86% compared to conventional methods.</p>

<h2>What are the shortcomings of current diagnostic tools?</h2>

<p>The first is PET imaging. These scans detect disease characteristics using radioactive tracers which light up areas of the brain where tangles and plaques may be present. However, PET scans are expensive, use radioactivity and require specialist facilities.</p>

<p>The second method uses a spinal tap to extract cerebrospinal fluid. This method is invasive and can be painful and stressful to patients.</p>

<p>Even traditional blood tests done in a clinic have limitations. These tests require immediate processing or refrigeration and careful handling. By contrast, the finger-prick test we&rsquo;re developing can be done at home and posted to a lab without refrigeration.</p>

<h2>What challenges have we encountered?</h2>

<p>Alzheimer&rsquo;s biomarker levels are often much lower in the blood than they are in cerebrospinal fluid. So the technological methods needed to measure them accurately had to be very sensitive.</p>

<p>Without refrigeration, the proteins can degrade &ndash; giving inaccurate readings and potentially misdiagnoses. So we&rsquo;re currently working to develop collection and mailing methods that ensure these dried blood proteins are stable.</p>

<p>Alzheimer&rsquo;s biomarkers are also not exclusive to the disease. Similar biomarkers can occur in other neurological conditions such as vascular dementia, multiple sclerosis, and even in otherwise asymptomatic people.</p>

<p>If validated, finger-prick tests could revolutionise Alzheimer&rsquo;s diagnosis. It would allow for earlier detection of the disease and broaden access for patients. The idea of diagnosing Alzheimer&rsquo;s with a quick, finger-prick test marks a profound shift in how we could approach neurodegenerative diseases.</p>
"""
    },
    'twins-longevity': {
        'title': 'What new twins study reveals about genes, environment and longevity',
        'author': 'Bradley Elliott',
        'author_initial': 'B',
        'date': '3 February 2026',
        'source': 'The Conversation',
        'tags': ['Science', 'Genetics', 'Health'],
        'content': """
<p>Why do some people live to 100 while their sibling dies decades earlier? Is it luck, lifestyle, or something written into their DNA?</p>

<p>Relative to many other species, humans are particularly long lived, but there is an ongoing argument about how much of our long lifespan is shaped by our genes and how much to our environment. It&rsquo;s the old &ldquo;nature versus nurture&rdquo; debate.</p>

<p>Researchers have repeatedly used large population studies to estimate how much genetics influences longevity. Historically, these studies have found relatively modest effects, typically around 25% to 33%, with some estimates as low as 6-16%.</p>

<p>A recent study published in <em>Science</em> challenged this trend, revising the estimate upward to about 50% by accounting for changes in external causes of death &ndash; such as accidents and infectious diseases &ndash; and separating the effects of genetics and environment in large historical cohorts of twins.</p>

<p>We know that individual genes affect lifespans in different species. A single mutation in the gene coding for the insulin sensor of worms would cause them to double their lifespan. Since that 1993 discovery, scientists have experimentally extended the lifespans of flies and mice, and even found hints of similar effects in long-lived humans.</p>

<p>This amount is more than an interesting number. If genetics mostly controls how long we live, then new anti-ageing treatments and lifestyle changes won&rsquo;t help much. But if genetics plays a smaller role, then what we do and the treatments we use could make a bigger difference.</p>

<h2>Nature&rsquo;s perfect experiment</h2>

<p>To tackle this question, the authors used data from the Swedish Adoption/Twin Study of Ageing. Because it includes a rare set of twins raised apart, the data makes it easier to tease apart the effects of genes and environment.</p>

<p>By studying monozygotic (&ldquo;identical&rdquo;) twins born between 1900 and 1935, the authors conclude that the inherited influence of lifespan is about 50%.</p>

<p>Put another way, about 50% of your potential lifespan is given to you by your parents, and the other 50% is the environment you live in. Things such as exercise, nutrition, sleep, stress, pollution and infectious disease exposure all fall into this external category.</p>

<p>The researchers then validated their models using data from populations in Denmark and the US. However, this also means the study populations were largely white, wealthy and European.</p>

<p>This doesn&rsquo;t mean that your personal actions aren&rsquo;t helping you &ndash; this debate probably isn&rsquo;t over yet. Even if genes account for about half our lifespan&rsquo;s story, the other half is still being written every day.</p>
"""
    },
    'plant-based-foods': {
        'title': 'How to keep plant-based foods on the table now that Veganuary is over',
        'author': 'Meera Iona Inglis',
        'author_initial': 'M',
        'date': '3 February 2026',
        'source': 'The Conversation',
        'tags': ['Food', 'Environment', 'Sustainability'],
        'content': """
<p>Campaigns like Veganuary (an initiative that encourages people to eat a plant-based diet in January) have been hugely successful in raising awareness about the climate and the health benefits of eating this way. However, making the switch longer term is not always easy &ndash; especially when there are usually limited meat-free options in workplaces.</p>

<p>For our recent study, my colleagues and I worked with Derek Bell (professor of environmental politics at Newcastle University) to identify public institutions like hospitals, universities and local councils as key players in the move towards a more sustainable food system. They account for a significant amount of the food that is sold in the UK &ndash; 5-6% of all food sales or &pound;2.4 billion annually.</p>

<p>However, getting caterers to become more plant-based can be controversial. Some argue that public institutions should not limit our freedom of choice when it comes to what we eat, or that it is insensitive to the cultural preferences of staff and clients.</p>

<p>Our work tries to tackle these concerns. While eliminating or reducing the offering of meat and dairy might limit options, public institutions already limit our choices in various ways to promote health and sustainability. Also, norms and expectations can change. The 2006 public smoking ban initially faced considerable resistance, but support for it has since greatly increased.</p>

<h2>Thoughtful catering</h2>

<p>When introduced thoughtfully, plant-based catering has proved popular. In 2021, New York City Health + Hospitals, the largest municipal health system in the US, made plant-based food the default option for its inpatient meals. Their menus are both nutritionally balanced and offer users a diverse range of choices. The menu includes Moroccan vegetable tagine, Spanish vegetable paella and a pad Thai noodle bowl.</p>

<p>As many as 95% of eligible patients did not request alternative meals, and 90% reported being satisfied. Many patients reported that they would continue to eat vegetarian meals at home. This shows the power of defaults, and the influence public institutions can have on our actions.</p>

<p>New York City Health + Hospitals has also shown tangible environmental and economic gains. Its food-related carbon emissions fell by 36%, while food bills also went down: these meals cost roughly 59 cents (&pound;0.43) less per tray than meat-based alternatives.</p>

<p>We&rsquo;re seeing changes happening elsewhere too. In the UK, a growing number of universities are gradually shifting towards more plant-based catering. In 2021, the four universities in Berlin successfully changed their menus to 68% vegan, 28% vegetarian and just 4% meat dishes.</p>

<p>Providing the right kinds of plant-based foods is an effective way of countering worries that people have about the health risks of going vegetarian or vegan, and about restricting their dietary preferences. In short, a well planned menu can keep plant-based foods on the table beyond Veganuary.</p>
"""
    },
}


@login_required
def exam_list(request):
    from .models import Course
    courses = Course.objects.all()
    return render(request, 'exams/exam_list.html', {'courses': courses})


@login_required
def listening_list(request):
    return render(request, 'exams/listening/list.html')


@login_required
def reading_list(request):
    return render(request, 'exams/reading/list.html')


@login_required
def writing_list(request):
    return render(request, 'exams/writing/list.html')


@login_required
def speaking_list(request):
    return render(request, 'exams/speaking/list.html')


@login_required
def practice_writing(request):
    return render(request, 'exams/writing/practice.html')


@login_required
def ai_assistant(request):
    return render(request, 'exams/ai/assistant.html')


def _call_azure_openai(prompt, system_instruction=""):
    api_key = settings.AZURE_OPENAI_API_KEY
    endpoint = settings.AZURE_OPENAI_ENDPOINT
    if not api_key or not endpoint:
        return None, "Azure OpenAI not configured. Set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT in .env file."

    client = AzureOpenAI(
        api_key=api_key,
        api_version=settings.AZURE_OPENAI_API_VERSION,
        azure_endpoint=endpoint,
    )

    messages = []
    if system_instruction:
        messages.append({"role": "system", "content": system_instruction})
    messages.append({"role": "user", "content": prompt})

    try:
        response = client.chat.completions.create(
            model=settings.AZURE_OPENAI_DEPLOYMENT_NAME,
            messages=messages,
            max_tokens=2000,
            temperature=0.7,
        )
        return response.choices[0].message.content, None
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg or "invalid_api_key" in error_msg.lower():
            return None, "API key is invalid. Please check your AZURE_OPENAI_API_KEY in .env file."
        elif "429" in error_msg:
            return None, "Rate limit reached. Please wait a moment and try again."
        elif "404" in error_msg or "DeploymentNotFound" in error_msg:
            return None, "Deployment not found. Check AZURE_OPENAI_DEPLOYMENT_NAME in .env file."
        else:
            return None, f"AI service error: {error_msg}"


@login_required
@require_POST
def ai_chat(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    message = data.get("message", "").strip()
    if not message:
        return JsonResponse({"error": "Empty message"}, status=400)

    system = (
        "You are an expert IELTS tutor and assistant. "
        "Help students with IELTS preparation including all four sections: Listening, Reading, Writing, and Speaking. "
        "Provide specific, actionable advice. Use examples when helpful. "
        "If asked to check writing, give band score estimates and specific feedback. "
        "Keep responses focused and practical. Format with paragraphs for readability. "
        "Do not use markdown formatting like ** or ## — use plain text only."
    )

    text, error = _call_azure_openai(message, system)
    if error:
        return JsonResponse({"error": error})

    return JsonResponse({"response": text})


@login_required
@require_POST
def ai_check_writing(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    essay = data.get("essay", "").strip()
    task_type = data.get("task_type", "Task 2")
    task_prompt = data.get("task_prompt", "")

    if not essay:
        return JsonResponse({"error": "No essay provided"}, status=400)

    word_count = len(essay.split())
    min_words = 150 if "1" in task_type else 250

    system = (
        "You are an experienced IELTS Writing examiner. "
        "Evaluate the essay based on the four IELTS Writing criteria: "
        "1) Task Achievement/Response, 2) Coherence and Cohesion, "
        "3) Lexical Resource, 4) Grammatical Range and Accuracy. "
        "Give an estimated band score (0.5 increments) for each criterion and an overall band. "
        "Provide specific feedback with examples from the essay. "
        "Suggest concrete improvements. Be encouraging but honest. "
        "Do not use markdown formatting like ** or ## — use plain text only. "
        "Structure your response clearly with the band scores at the top."
    )

    prompt = f"""IELTS Writing {task_type} Evaluation

Task prompt: {task_prompt}

Student's essay ({word_count} words, minimum required: {min_words}):

{essay}

Please evaluate this essay."""

    text, error = _call_azure_openai(prompt, system)
    if error:
        return JsonResponse({"error": error})

    return JsonResponse({"feedback": text, "word_count": word_count})


@login_required
def articles_list(request):
    return render(request, 'exams/articles/list.html')


@login_required
def article_view(request, slug):
    article = ARTICLES.get(slug)
    if not article:
        raise Http404("Article not found")
    return render(request, 'exams/articles/detail.html', {'article': article})


@login_required
def start_exam(request, exam_id):
    exam_set = get_object_or_404(ExamSet, id=exam_id, is_active=True)
    attempt = ExamAttempt.objects.create(
        user=request.user,
        exam_set=exam_set,
        current_section='listening',
    )
    return redirect('exams:section', attempt_id=attempt.id, section_type='listening')


@login_required
def exam_section(request, attempt_id, section_type):
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, user=request.user)
    if attempt.status == 'completed':
        return redirect('results:detail', attempt_id=attempt.id)

    section = get_object_or_404(Section, exam_set=attempt.exam_set, section_type=section_type)
    questions = section.questions.all()

    # Set section start time
    start_field = f'{section_type}_start'
    if not getattr(attempt, start_field):
        setattr(attempt, start_field, timezone.now())
        attempt.current_section = section_type
        attempt.save()

    # Get existing responses
    existing = {}
    for resp in StudentResponse.objects.filter(attempt=attempt, question__section=section):
        existing[resp.question_id] = resp.answer_text

    # Calculate remaining time
    section_start = getattr(attempt, start_field)
    elapsed = (timezone.now() - section_start).total_seconds()
    remaining = max(0, section.duration_minutes * 60 - elapsed)

    context = {
        'attempt': attempt,
        'section': section,
        'questions': questions,
        'existing': existing,
        'remaining_seconds': int(remaining),
        'section_type': section_type,
    }

    if section_type == 'reading':
        context['passages'] = section.passages.all()

    template = f'exams/{section_type}.html'
    return render(request, template, context)


@login_required
@require_POST
def auto_save(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, user=request.user)
    if attempt.status == 'completed':
        return JsonResponse({'status': 'error', 'message': 'Exam already completed'})

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid data'})

    answers = data.get('answers', {})
    for q_id, answer in answers.items():
        try:
            question = Question.objects.get(id=int(q_id))
        except (Question.DoesNotExist, ValueError):
            continue
        StudentResponse.objects.update_or_create(
            attempt=attempt,
            question=question,
            defaults={'answer_text': answer}
        )

    return JsonResponse({'status': 'ok', 'saved': len(answers)})


@login_required
@require_POST
def submit_section(request, attempt_id, section_type):
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, user=request.user)
    if attempt.status == 'completed':
        return redirect('results:detail', attempt_id=attempt.id)

    section = get_object_or_404(Section, exam_set=attempt.exam_set, section_type=section_type)

    # Save final answers
    for key, value in request.POST.items():
        if key.startswith('question_'):
            q_id = key.replace('question_', '')
            try:
                question = Question.objects.get(id=int(q_id))
            except (Question.DoesNotExist, ValueError):
                continue
            StudentResponse.objects.update_or_create(
                attempt=attempt,
                question=question,
                defaults={'answer_text': value}
            )

    # Set end time
    end_field = f'{section_type}_end'
    setattr(attempt, end_field, timezone.now())
    attempt.save()

    # Determine next section
    section_order = ['listening', 'reading', 'writing', 'speaking']
    current_idx = section_order.index(section_type)

    if current_idx < len(section_order) - 1:
        next_section = section_order[current_idx + 1]
        # Check if next section exists
        if Section.objects.filter(exam_set=attempt.exam_set, section_type=next_section).exists():
            return redirect('exams:section', attempt_id=attempt.id, section_type=next_section)

    # All sections done - complete exam
    attempt.status = 'completed'
    attempt.completed_at = timezone.now()
    attempt.save()

    _calculate_results(attempt)
    return redirect('results:detail', attempt_id=attempt.id)


def _calculate_results(attempt):
    from results.models import ExamResult

    result, _ = ExamResult.objects.get_or_create(attempt=attempt, user=attempt.user)

    # Score listening
    listening_responses = StudentResponse.objects.filter(
        attempt=attempt, question__section__section_type='listening'
    )
    l_correct = 0
    for resp in listening_responses:
        if resp.question.correct_answer and resp.answer_text.strip().lower() == resp.question.correct_answer.strip().lower():
            resp.is_correct = True
            l_correct += 1
        else:
            resp.is_correct = False
        resp.save()
    result.listening_correct = l_correct
    result.listening_score = _raw_to_band(l_correct, 40)

    # Score reading
    reading_responses = StudentResponse.objects.filter(
        attempt=attempt, question__section__section_type='reading'
    )
    r_correct = 0
    for resp in reading_responses:
        if resp.question.correct_answer and resp.answer_text.strip().lower() == resp.question.correct_answer.strip().lower():
            resp.is_correct = True
            r_correct += 1
        else:
            resp.is_correct = False
        resp.save()
    result.reading_correct = r_correct
    result.reading_score = _raw_to_band(r_correct, 40)

    # Writing and speaking scored as N/A (manual grading needed)
    result.writing_score = None
    result.speaking_score = None

    # Calculate time spent
    if attempt.listening_start and attempt.listening_end:
        result.time_listening = int((attempt.listening_end - attempt.listening_start).total_seconds())
    if attempt.reading_start and attempt.reading_end:
        result.time_reading = int((attempt.reading_end - attempt.reading_start).total_seconds())
    if attempt.writing_start and attempt.writing_end:
        result.time_writing = int((attempt.writing_end - attempt.writing_start).total_seconds())
    if attempt.speaking_start and attempt.speaking_end:
        result.time_speaking = int((attempt.speaking_end - attempt.speaking_start).total_seconds())

    result.save()
    result.calculate_overall_band()


def _raw_to_band(correct, total):
    if total == 0:
        return 0
    ratio = correct / total
    if ratio >= 0.975:
        return 9.0
    elif ratio >= 0.925:
        return 8.5
    elif ratio >= 0.875:
        return 8.0
    elif ratio >= 0.825:
        return 7.5
    elif ratio >= 0.75:
        return 7.0
    elif ratio >= 0.675:
        return 6.5
    elif ratio >= 0.6:
        return 6.0
    elif ratio >= 0.525:
        return 5.5
    elif ratio >= 0.45:
        return 5.0
    elif ratio >= 0.375:
        return 4.5
    elif ratio >= 0.3:
        return 4.0
    elif ratio >= 0.225:
        return 3.5
    elif ratio >= 0.15:
        return 3.0
    else:
        return 2.5


@login_required
def practice_reading(request):
    return render(request, 'exams/reading/practice.html')


@login_required
def practice_listening(request):
    return render(request, 'exams/listening/practice.html')


@login_required
@require_POST
def upload_speaking(request, attempt_id, question_id):
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, user=request.user)
    question = get_object_or_404(Question, id=question_id)

    audio_file = request.FILES.get('audio')
    if not audio_file:
        return JsonResponse({'status': 'error', 'message': 'No audio file'})

    resp, _ = StudentResponse.objects.get_or_create(attempt=attempt, question=question)
    resp.audio_file = audio_file
    resp.answer_text = '[audio recorded]'
    resp.save()

    return JsonResponse({'status': 'ok'})
