from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Q
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
import requests

from .forms import MemoForm, SubjectForm
from .models import Memo, Subject


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("memo_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def memo_list(request):
    qs = Memo.objects.filter(user=request.user).select_related("subject")

    
    q = request.GET.get("q", "").strip()
    subject_id = request.GET.get("subject", "").strip()
    imp = request.GET.get("imp", "").strip()  
    fav = request.GET.get("fav", "").strip()  

    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(tags__icontains=q))
    if subject_id:
        qs = qs.filter(subject_id=subject_id)
    if imp:
        try:
            qs = qs.filter(importance=int(imp))
        except ValueError:
            pass
    if fav == "1":
        qs = qs.filter(is_favorite=True)

    subjects = Subject.objects.filter(user=request.user)

    return render(
        request,
        "memos/memo_list.html",
        {
            "memos": qs,
            "subjects": subjects,
            "filters": {"q": q, "subject": subject_id, "imp": imp, "fav": fav},
        },
    )


@login_required
def memo_detail(request, pk):
    memo = get_object_or_404(Memo, pk=pk, user=request.user)
    return render(request, "memos/memo_detail.html", {"memo": memo})


@login_required
def memo_create(request):
    if request.method == "POST":
        form = MemoForm(request.POST)
        if form.is_valid():
            memo = form.save(commit=False)
            memo.user = request.user
            memo.save()
            return redirect("memo_detail", pk=memo.pk)
    else:
        form = MemoForm()

    
    form.fields["subject"].queryset = Subject.objects.filter(user=request.user)

    return render(request, "memos/memo_form.html", {"form": form, "mode": "create"})


@login_required
def memo_update(request, pk):
    memo = get_object_or_404(Memo, pk=pk, user=request.user)
    if request.method == "POST":
        form = MemoForm(request.POST, instance=memo)
        if form.is_valid():
            form.save()
            return redirect("memo_detail", pk=memo.pk)
    else:
        form = MemoForm(instance=memo)

    form.fields["subject"].queryset = Subject.objects.filter(user=request.user)

    return render(request, "memos/memo_form.html", {"form": form, "mode": "edit", "memo": memo})


@login_required
def memo_delete(request, pk):
    memo = get_object_or_404(Memo, pk=pk, user=request.user)
    if request.method == "POST":
        memo.delete()
        return redirect("memo_list")
    return render(request, "memos/memo_confirm_delete.html", {"memo": memo})


@login_required
def subject_create(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)
        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()
            return redirect("memo_create")
    else:
        form = SubjectForm()
    return render(request, "memos/subject_form.html", {"form": form})



@login_required
def memo_favorite_toggle(request, pk):
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)

    memo = get_object_or_404(Memo, pk=pk, user=request.user)
    memo.is_favorite = not memo.is_favorite
    memo.save(update_fields=["is_favorite"])
    return JsonResponse({"ok": True, "is_favorite": memo.is_favorite})



@login_required
def study_tip_api(request):
    try:
        r = requests.get("https://zenquotes.io/api/random", timeout=10)
        r.raise_for_status()
        data = r.json()[0]
        tip = f"{data.get('q','')} — {data.get('a','')}".strip()
    except Exception:
        tip = "今日は短時間でも継続しよう"

    return JsonResponse({"tip": tip})

