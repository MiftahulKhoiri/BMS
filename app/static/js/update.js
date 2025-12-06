// Animasi progress bar
function progressTo(percent) {
    document.getElementById("progressBar").style.width = percent + "%";
}

async function checkUpdate() {
    progressTo(20);
    document.getElementById("updateStatus").innerText = "Mengecek versi di GitHub...";

    let res = await fetch("/update/check");
    let data = await res.json();

    progressTo(50);

    if (data.update_available) {
        document.getElementById("updateStatus").innerText =
            `Update tersedia! Versi ${data.github_version}`;
    } else {
        document.getElementById("updateStatus").innerText =
            "Server sudah versi terbaru.";
    }

    progressTo(100);
    setTimeout(() => progressTo(0), 800); // reset bar
}

async function applyUpdate() {
    if (!confirm("Yakin ingin melakukan update server?")) return;

    document.getElementById("updateStatus").innerText = "Mengambil update dari GitHub...";
    progressTo(10);

    let res = await fetch("/update/apply", {
        method: "POST"
    });

    progressTo(60);

    let data = await res.json();

    if (data.ok) {
        document.getElementById("updateStatus").innerText = "Update berhasil diterapkan!";
        progressTo(100);
    } else {
        document.getElementById("updateStatus").innerText =
            "Update gagal: " + (data.error || "Tidak diketahui");
        progressTo(0);
    }

    // reset bar perlahan
    setTimeout(() => progressTo(0), 1200);
}