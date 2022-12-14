import re
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from models import *
from forms import *

def home(request):
	return redirect('hanzi_show', 'rsh1', '10')

def guestbook(request):
    return render(request, 'guwen/guestbook.html')

def cedict_update(request):
    if request.method == 'POST':
        form = CedictUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            CedictDataSingle.update(request.FILES['cedict_gz'])
            LexicalEntry.update_all()
            messages.success(request, 'Successfully updated the lexical data with the provided cedict file!')
            return redirect('home')
    else:
        form = CedictUpdateForm()
    return render(request, 'guwen/cedict_update.html', {
        'form': form,
        })

def hanzi_show(request, heisigBook, heisigID):
    hanzi = get_object_or_404(Hanzi, heisigBook=heisigBook, heisigID=heisigID)
    termElements = list(hanzi.termElements.all())
    hanziComponents = []
    for te in termElements:
        hanziComponent = te.getHanziPrimitive()
        hanziComponent.setSelTermPrimitiveMeaning(te.term)
        hanziComponents.append(hanziComponent)
    hanziUsers = []
    for t in hanzi.getKeywordPrimitiveMeanings():
        hanziUsers += t.hanziUsers.all()
    # TODO: deepsearch

    try:
        prev_hanzi = Hanzi.objects.get(
            heisigBook=hanzi.heisigBook,
            heisigFrame=hanzi.heisigFrame - 1,
            heisigFrame__gt=0,
            )
    except Hanzi.DoesNotExist:
        prev_hanzi = None

    try:
        next_hanzi = Hanzi.objects.get(
            heisigBook=hanzi.heisigBook,
            heisigFrame=hanzi.heisigFrame + 1,
            )
    except Hanzi.DoesNotExist:
        next_hanzi = None

    return render(request, 'guwen/hanzi_show.html', {
        'hanzi': hanzi, 
        'termElements': termElements,
        'hanziComponents': hanziComponents,
        'hanziUsers': hanziUsers,
        'hanziPrimitiveMeanings': hanzi.termPrimitiveMeanings.all(),
        'prev_hanzi': prev_hanzi,
        'next_hanzi': next_hanzi,
        })

def search(request):
    if 'input_search' not in request.GET:
        return redirect('hanzi_list')

    # search logic to be put elsewhere tbd. ... 
    search_term = request.GET['input_search']

    if not search_term:
        return redirect('home')
        
    # search for hanzi
    if len(search_term) == 1:
        try:
            hanzi = Hanzi.objects.get(char=search_term[0].encode('utf8'))
        except Hanzi.DoesNotExist:
            messages.info(request, '"{}" not in database.'.format(search_term[0].encode('utf8')))
            return redirect('hanzi_list')
        return redirect('hanzi_show', hanzi.heisigBook, hanzi.heisigID)
    # search for Heisig Frame no
    if search_term.isdigit():
        search_term = int(search_term)
    	if search_term <= HanziMeta.objects.latest().maxHeisigID // 10:
            hanzi = get_object_or_404(Hanzi, heisigFrame=search_term)
            return redirect('hanzi_show', hanzi.heisigBook, hanzi.heisigID)
        else:
            messages.info(request, 'Heisig frame No. {} not in database.'.format(search_term))
            return redirect('hanzi_list')
    # match pinyin with numbered tones
    if re.match('[a-zA-Z]+\d', search_term, flags=re.UNICODE):
        pinyinWOTone = search_term[:-1]
        tone = search_term[-1]
        try:
            syllable = Syllable.objects.get(pinyinWOTone=pinyinWOTone, tone=tone)
        except Syllable.DoesNotExist:
            messages.info(request, 'Syllable {} not in database.'.format(search_term))
            return redirect('hanzi_list')
        hanzi_list = syllable.hanzis.all()
    # match pinyin with tone accents
    else:
        syllables = Syllable.objects.filter(pinyin=search_term)
    	hanzi_list = []
        for syllable in syllables:
            hanzi_list.extend(syllable.hanzis.all())
        # search in pinyin w/o tone
        syllables = Syllable.objects.filter(pinyinWOTone=search_term)
        for syllable in syllables:
            hanzi_list.extend(syllable.hanzis.all())
        # search in keywords and primitive meanings
        # django_like causes crashes tbd.
        terms = EnglishTerm.objects.filter(
            term__contains=search_term,
            term=search_term,
            )
        for term in terms:
            if term.hanziPrimitive_id is None:
                hanzi_list.append(term.hanziCharacter)
            else:
                hanzi_list.append(term.hanziPrimitive)
        
    messages.info(request, 'Searching for "{}" gave {} results.'.format(
        search_term,
        len(hanzi_list),
        ))
    context = {
        'hanzi_list': hanzi_list,
        'my_url': request.path,
        }
    return render(request, 'guwen/search_results.html', context)

def hanzi_list(request):
    hanzi_list = Hanzi.objects.all().order_by('heisigID')
    # Show 25 hanzis per page.
    paginator = Paginator(hanzi_list, 15)

    page = request.GET.get('page')
    try:
        hanzis = paginator.page(page)
    except PageNotAnInteger:
        hanzis = paginator.page(1)
    except EmptyPage:
        hanzis = paginator.page(paginator.num_pages)

    context = {
        'hanzi_list': hanzis,
        'my_url': request.path
    }

    return render(request, 'guwen/hanzi_list.html', context)

def hanzi_edit(request, pk):
    hanzi = get_object_or_404(Hanzi, pk=pk)
    if request.method == 'POST':
        form = HanziEditForm(data=request.POST, instance=hanzi)
        if form.is_valid():
            form.save()
            return redirect('hanzi_show', hanzi.heisigBook, hanzi.heisigID)
    else:
        form = HanziEditForm(instance=hanzi)
    return render(request, 'guwen/hanzi_edit.html', {
        'hanzi': hanzi,
        'form': form,
        })

def hanzi_add(request):
    if request.method == 'POST':
        form = HanziAddForm(data=request.POST)
    	if form.is_valid():
            hanzi = form.save()
    	    return redirect('hanzi_show', hanzi.heisigBook, hanzi.heisigID)
    else:
        try:
            hanzi = Hanzi.objects.latest('date_created')
            hanzi.pk = None
            hanzi.heisigFrame += 1
            hanzi.heisigID += 10
            hanzi.char = ''
            hanzi.numStrokes = None
        except Hanzi.DoesNotExist:
            hanzi = None
        form = HanziAddForm(instance=hanzi)
    return render(request, 'guwen/hanzi_edit.html', {
        'form': form,
        })

def lexical_data_update(request):
    LexicalEntry.update_all()
    return redirect(request.GET.get('next', 'hanzi_list'))
    
def convert_pinyin_all(request):
    LexicalEntry.convert_pinyin_all()
    return redirect(request.GET.get('next', 'hanzi_list'))
