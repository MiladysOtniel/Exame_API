document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('registerForm');
    const loginForm = document.getElementById('loginForm');
    const usersTableBody = document.getElementById('usersTableBody');

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const username = document.getElementById('registerUsername').value;
            const email = document.getElementById('registerEmail').value;
            const password = document.getElementById('registerPassword').value;

            try {
                const response = await fetch('http://localhost:5000/api/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ username, email, password })
                });

                const result = await response.json();
                document.getElementById('registerMessage').textContent = result.message || result.error;
            } catch (error) {
                console.error('Erro no registro:', error);
            }
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;

            try {
                const response = await fetch('http://localhost:5000/api/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                const result = await response.json();
                document.getElementById('loginMessage').textContent = result.message || result.error;
                if(response.status == 200){
                    window.location.href = 'admin.html';
                }
            } catch (error) {
                console.error('Erro no login:', error);
            }
        });
    }

    function logout(userId) {
        fetch(`http://localhost:5000/api/logout/${userId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao fazer logout.');
                }
                return response.json();
            })
            .then(result => {
                console.log(result.message);
                window.location.href = '/login.html';
            })
            .catch(error => console.error('Erro ao fazer logout:', error));
    }

    if (usersTableBody) {
        fetch('http://localhost:5000/api/users')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Erro ao buscar usuários.');
                }
                return response.json();
            })
            .then(users => {
                users.forEach(user => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${user.id}</td>
                        <td>${user.username}</td>
                        <td>${user.email}</td>
                        <td><button onclick="logout(${user.id})">Logout</button></td>
                    `;
                    usersTableBody.appendChild(row);
                });
            })
            .catch(error => console.error('Erro ao buscar usuários:', error));
    }
});