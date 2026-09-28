import flet as ft
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_ANON_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

def main(page: ft.Page):
    page.title = "ملتقى الفكر"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    status_text = ft.Text("جاري التحقق من الإشعارات...", size=16)

    def save_fcm_token_to_supabase(token: str):
        try:
            response = supabase.table("devices").insert({
                "user_id": "default_user",
                "fcm_token": token
            }).execute()

            status_text.value = "تم تفعيل استقبال الإشعارات بنجاح! ✅"
            page.update()
        except Exception as e:
            status_text.value = f"حدث خطأ أثناء الحفظ: {e}"
            page.update()

    def get_device_token(e):
        sample_token = "TEST_TOKEN_DEVICE_12345"
        status_text.value = "جاري إرسال الرمز إلى قاعدة البيانات..."
        page.update()
        save_fcm_token_to_supabase(sample_token)

    page.add(
        ft.Column([
            ft.Text("مرحباً بك في تطبيق ملتقى الفكر", size=22, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),
            status_text,
            ft.Container(height=20),
            ft.ElevatedButton(
                text="تفعيل الإشعارات الآن",
                icon=ft.icons.NOTIFICATIONS_ACTIVE,
                on_click=get_device_token
            )
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    )

ft.app(target=main)
