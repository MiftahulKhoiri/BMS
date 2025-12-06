async function loadUsers() {
    let res = await fetch("/users");
    let data = await res.json();

    let table = document.querySelector("#userTable tbody");
    table.innerHTML = "";

    data.forEach(u => {
        table.innerHTML += `
        <tr>
            <td>${u.id}</td>
            <td>${u.username}</td>
            <td>${u.email}</td>
            <td>${u.role}</td>
            <td>${u.status}</td>
            <td>
                <a class="action-btn" href="/users/update/${u.id}">Edit</a>
                <a class="action-btn" href="/users/delete/${u.id}">Hapus</a>
            </td>
        </tr>
        `;
    });
}

loadUsers();