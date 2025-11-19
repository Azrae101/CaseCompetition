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
    // Helper to get the form action filename (last path segment)
    function formActionName(form){
        if(!form || !form.getAttribute) return '';
        let a = form.getAttribute('action') || '';
        try{ a = new URL(a, window.location.href).pathname; }catch(e){}
        const parts = a.split('/').filter(Boolean);
        return parts.length? parts[parts.length-1] : '';
    }

    // Intercept forms by action filename ending
    Array.from(document.querySelectorAll('form')).forEach(function(f){
        const name = formActionName(f).toLowerCase();
        if(name.includes('login')){
            f.addEventListener('submit', function(e){
                e.preventDefault();
                const user = document.getElementById('username') ? document.getElementById('username').value : 'user';
                localStorage.setItem('logged_in','true');
                localStorage.setItem('username', user);
                // redirect to home
                window.location.href = '/';
            });
        }
        if(name.includes('register')){
            f.addEventListener('submit', function(e){
                e.preventDefault();
                const user = document.getElementById('username') ? document.getElementById('username').value : 'newuser';
                localStorage.setItem('username', user);
                alert('Registered (fake). You will be redirected to login.');
                window.location.href = '/login.html';
            });
        }
        if(name.includes('profile')){
            f.addEventListener('submit', function(e){
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
            const fval = localStorage.getItem('user_first');
            if(fval && document.getElementById('first_name')) document.getElementById('first_name').value = fval;
            const lval = localStorage.getItem('user_last');
            if(lval && document.getElementById('last_name')) document.getElementById('last_name').value = lval;
            const evalv = localStorage.getItem('user_email');
            if(evalv && document.getElementById('email')) document.getElementById('email').value = evalv;
        }
    });

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
