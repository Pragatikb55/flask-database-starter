async function addBookAPI() {
    const data = {
        title: document.getElementById("title").value,
        isbn: document.getElementById("isbn").value,
        author_id: document.getElementById("author").value
    };

    const res = await fetch('/api/add-book', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    const result = await res.json();
    if (result.success) {
        alert("Book added using API!");
        location.reload();
    }
}
