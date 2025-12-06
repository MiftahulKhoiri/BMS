async function saveProfile() {
    let full_name = document.querySelector("#full_name").value;
    let phone = document.querySelector("#phone").value;
    let address = document.querySelector("#address").value;

    let res = await fetch(`/users/update/{{ user.id }}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ full_name, phone, address })
    });

    let data = await res.json();
    alert("Profil berhasil disimpan");
}