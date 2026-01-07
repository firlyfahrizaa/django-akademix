import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .models import DeviceUser, Note, Matkul

# Helper: Cari user berdasarkan ID HP, kalau belum ada otomatis dibuatkan
def get_user_from_request(request):
    device_id = request.headers.get('X-Device-ID')
    if not device_id:
        return None
    user, created = DeviceUser.objects.get_or_create(device_id=device_id)
    return user

# --- API NOTES ---
@csrf_exempt
def notes_api(request):
    user = get_user_from_request(request)
    if not user:
        return JsonResponse({'error': 'No Device ID header'}, status=400)

    if request.method == 'GET':
        # ... kode GET lama ...
        notes = list(user.notes.values('id', 'title', 'content', 'color', 'created_at').order_by('-updated_at'))
        return JsonResponse(notes, safe=False)

    elif request.method == 'POST':
        # ... kode POST lama ...
        data = json.loads(request.body)
        note = Note.objects.create(
            user=user,
            title=data.get('title', 'Tanpa Judul'),
            content=data.get('content', ''),
            color=data.get('color', 'bg-yellow-100')
        )
        return JsonResponse({'id': note.id, 'status': 'saved'})

    # --- TAMBAHKAN BAGIAN INI (PUT) ---
    elif request.method == 'PUT':
        data = json.loads(request.body)
        note_id = data.get('id')
        try:
            # Cari note yang ID-nya cocok DAN punya user ini (biar gak ngedit punya orang)
            note = Note.objects.get(id=note_id, user=user)
            note.title = data.get('title', note.title)
            note.content = data.get('content', note.content)
            note.save()
            return JsonResponse({'status': 'updated'})
        except Note.DoesNotExist:
            return JsonResponse({'error': 'Note not found'}, status=404)
    # ----------------------------------

    elif request.method == 'DELETE':
        # ... kode DELETE lama ...
        data = json.loads(request.body)
        note_id = data.get('id')
        Note.objects.filter(id=note_id, user=user).delete()
        return JsonResponse({'status': 'deleted'})

    return JsonResponse({'error': 'Method not allowed'}, status=405)

# --- API IPK ---
@csrf_exempt
def ipk_api(request):
    user = get_user_from_request(request)
    if not user:
        return JsonResponse({'error': 'No Device ID header'}, status=400)

    if request.method == 'GET':
        matkuls = list(user.matkuls.values('id', 'name', 'sks', 'grade').order_by('-created_at'))
        return JsonResponse(matkuls, safe=False)

    elif request.method == 'POST':
        data = json.loads(request.body)
        matkul = Matkul.objects.create(
            user=user,
            name=data.get('name'),
            sks=data.get('sks'),
            grade=data.get('grade')
        )
        return JsonResponse({'id': matkul.id, 'status': 'saved'})
    
    elif request.method == 'DELETE':
        data = json.loads(request.body)
        matkul_id = data.get('id')
        Matkul.objects.filter(id=matkul_id, user=user).delete()
        return JsonResponse({'status': 'deleted'})

    return JsonResponse({'error': 'Method not allowed'}, status=405)