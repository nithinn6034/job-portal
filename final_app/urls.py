
from django.urls import  path



from final_app import views


urlpatterns = [

    path('',views.display,name='display'),
    path('login_load_user',views.login_load_user,name='login_load_user'),
    path('signup_load_user',views.signup_load_user,name='signup_load_user'),
    path('login_load_admin',views.login_load_admin,name='login_load_admin'),
    path('signup_load_admin',views.signup_load_admin,name='signup_load_admin'),
    path('usersignup_load',views.usersignup_load,name='usersignup_load'),
    path('userfront_load',views.userfront_load,name='userfront_load'),
    path('userlog_load',views.userlog_load,name='userlog_load'),
    path('adminsignup_load',views.adminsignup_load,name='adminsignup_load'),
    path('adminfront_load',views.adminfront_load,name='adminfront_load'),
    path('adminlog_load',views.adminlog_load,name='adminlog_load'),
    path('addjobadmin',views.addjobadmin,name='addjobadmin'),
    path('job_applied_admin',views.job_applied_admin,name='job_applied_admin'),
    path('view_user_pro_admin',views.view_user_pro_admin,name='view_user_pro_admin'),
    path('personal_detail_admin',views.personal_detail_admin,name='personal_detail_admin'),
    path('added_job_list',views.added_job_list,name='added_job_list'),
    path('add_job',views.add_job,name='add_job'),
    path('add_det_for_jobuser',views.add_det_for_jobuser,name='add_det_for_jobuser'),
    path('vac_of_job',views.vac_of_job,name='vac_of_job'),
    path('det_fo_jobuser_save',views.det_fo_jobuser_save,name='det_fo_jobuser_save'),
    path('view_resume_user',views.view_resume_user,name='view_resume_user'),
    path('user_detail_user',views.user_detail_user,name='user_detail_user'),
    path('apply_now/<int:pk>/', views.apply_now, name='apply_now'),
    path('main_admin',views.main_admin,name='main_admin'),
    path('add_job_list_edit/<int:pk>/',views.add_job_list_edit,name='add_job_list_edit'),
    path('add_job_list_edit_load/<int:pk>/',views.add_job_list_edit_load,name='add_job_list_edit_load'),
    path('add_job_list_delete/<int:pk>/',views.add_job_list_delete,name='add_job_list_delete'),
    path('add_job_list_delete_load/<int:pk>/',views.add_job_list_delete_load,name='add_job_list_delete_load'),
    path('personal_detail_admin_edit/<int:pk>/',views.personal_detail_admin_edit,name='personal_detail_admin_edit'),
    path('personal_detail_admin_edit_load/<int:pk>/',views.personal_detail_admin_edit_load,name='personal_detail_admin_edit_load'),
    path('view_resume_user_edit/<int:pk>/',views.view_resume_user_edit,name='view_resume_user_edit'),
    path('view_resume_user_edit_load/<int:pk>/',views.view_resume_user_edit_load,name='view_resume_user_edit_load'),
    path('recru_list_main',views.recru_list_main,name='recru_list_main'),
    path('recru_list_main_edit/<int:pk>/',views.recru_list_main_edit,name='recru_list_main_edit'),
    path('recru_list_main_edit_load/<int:pk>/',views.recru_list_main_edit_load,name='recru_list_main_edit_load'),
    path('recru_list_main_delete/<int:pk>/',views.recru_list_main_delete,name='recru_list_main_delete'),
    path('recru_list_main_delete_load/<int:pk>/',views.recru_list_main_delete_load,name='recru_list_main_delete_load'),
    path('job_seeker_list_main',views.job_seeker_list_main,name='job_seeker_list_main'),
    path('job_seeker_list_main_edit/<int:pk>/',views.job_seeker_list_main_edit,name='job_seeker_list_main_edit'),
    path('job_seeker_list_main_edit_load/<int:pk>/',views.job_seeker_list_main_edit_load,name='job_seeker_list_main_edit_load'),
    path('jobseeker_main_delete/<int:pk>/', views.jobseeker_main_delete, name='jobseeker_main_delete'),
    path('jobseeker_main_delete_load/<int:pk>/', views.jobseeker_main_delete_load, name='jobseeker_main_delete_load'),
    path('job_list_main',views.job_list_main,name='job_list_main'),
    path('job_list_main_edit/<int:pk>/',views.job_list_main_edit,name='job_list_main_edit'),
    path('job_list_main_edit_load/<int:pk>/',views.job_list_main_edit_load,name='job_list_main_edit_load'),
    path('job_list_main_delete/<int:pk>/',views.job_list_main_delete,name='job_list_main_delete'),
    path('user_detail_user_edit/<int:pk>/',views.user_detail_user_edit,name='user_detail_user_edit'),
    path('user_detail_user_edit_load/<int:pk>/',views.user_detail_user_edit_load,name='user_detail_user_edit_load'),
    path('logout/', views.logout_view, name='logout'),\
    path('tracker_user',views.tracker_user,name='tracker_user'),
    path('view_user_pro_admin_edit/<int:pk>/',views.view_user_pro_admin_edit,name='view_user_pro_admin_edit'),
    path('view_user_pro_admin_edit_load/<int:pk>/',views.view_user_pro_admin_edit_load,name='view_user_pro_admin_edit_load'),
    path('view_user_pro_admin_delete/<int:pk>/', views.view_user_pro_admin_delete, name='view_user_pro_admin_delete'),
    path('about',views.about,name='about')
]

