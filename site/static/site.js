// Client-side helper for fake login/register/profile persistence.
document.addEventListener('DOMContentLoaded', function(){
    const isLoggedIn = localStorage.getItem('logged_in') === 'true';
    const username = localStorage.getItem('username') || '';

    const navLogin = document.getElementById('nav-login');
    const navRegister = document.getElementById('nav-register');
    const navProfile = document.getElementById('nav-profile');
    const navLogout = document.getElementById('nav-logout');
    const profileBtn = document.getElementById('profile-btn');
    const navStreak = document.getElementById('nav-streak');
    const streakNumber = document.getElementById('streak-number');

    function refreshNav(){
        const logged = localStorage.getItem('logged_in') === 'true';
        if(logged){
            if(navLogin) navLogin.style.display='none';
            if(navRegister) navRegister.style.display='none';
            if(navProfile) navProfile.style.display='inline-block';
            if(navStreak) navStreak.style.display='inline-flex';
            if(profileBtn) profileBtn.textContent = (localStorage.getItem('username')||'P').slice(0,1).toUpperCase();
            if(streakNumber) streakNumber.textContent = localStorage.getItem('streak') || '5';
        } else {
            if(navLogin) navLogin.style.display='inline-block';
            if(navRegister) navRegister.style.display='none';
            if(navProfile) navProfile.style.display='none';
            if(navStreak) navStreak.style.display='none';
        }
    }

    refreshNav();

    // Intercept login form if present
    const loginForm = document.querySelector('form[action="/login"]');
    if(loginForm){
        loginForm.addEventListener('submit', function(e){
            e.preventDefault();
            const user = document.getElementById('username') ? document.getElementById('username').value : 'user';
            localStorage.setItem('logged_in','true');
            localStorage.setItem('username', user);
            // redirect to home
            window.location.href = '/';
        });
    }

    // Intercept register form
    const registerForm = document.querySelector('form[action="/register"]');
    if(registerForm){
        registerForm.addEventListener('submit', function(e){
            e.preventDefault();
            // store the username locally (fake)
            const user = document.getElementById('username') ? document.getElementById('username').value : 'newuser';
            localStorage.setItem('username', user);
            // show flash and redirect to login
            alert('Registered (fake). You will be redirected to login.');
            window.location.href = '/login';
        });
    }

    // Intercept profile settings form to save fields to localStorage
    const profileForm = document.querySelector('form[action="/profile/settings"]');
    if(profileForm){
        profileForm.addEventListener('submit', function(e){
            e.preventDefault();
            const first = document.getElementById('first_name') ? document.getElementById('first_name').value : '';
            const last = document.getElementById('last_name') ? document.getElementById('last_name').value : '';
            const email = document.getElementById('email') ? document.getElementById('email').value : '';
            localStorage.setItem('user_first', first);
            localStorage.setItem('user_last', last);
            localStorage.setItem('user_email', email);
            alert('Profile saved locally (fake).');
        });
        // populate fields if saved
        const f = localStorage.getItem('user_first');
        if(f) document.getElementById('first_name').value = f;
        const l = localStorage.getItem('user_last');
        if(l) document.getElementById('last_name').value = l;
        const em = localStorage.getItem('user_email');
        if(em) document.getElementById('email').value = em;
    }

    // Logout handler
    if(navLogout){
        navLogout.addEventListener('click', function(e){
            e.preventDefault();
            localStorage.removeItem('logged_in');
            // Optionally remove username
            // localStorage.removeItem('username');
            refreshNav();
            window.location.href = '/';
        });
    }

    // If there's an explicit logout link (e.g., /logout), intercept anchor clicks
    document.querySelectorAll('a[href="/logout"]').forEach(function(a){
        a.addEventListener('click', function(e){ e.preventDefault(); localStorage.removeItem('logged_in'); refreshNav(); window.location.href = '/'; });
    });

});
