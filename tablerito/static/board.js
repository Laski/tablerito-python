// Drag a card to another list: the drop submits the card's hidden move form.
let dragged = null;

for (const card of document.querySelectorAll(".card")) {
  card.draggable = true;
  card.addEventListener("dragstart", (event) => {
    dragged = card;
    event.dataTransfer.effectAllowed = "move";
    event.dataTransfer.setData("text/plain", "");
    card.classList.add("dragging");
  });
  card.addEventListener("dragend", () => {
    card.classList.remove("dragging");
    dragged = null;
  });
}

for (const list of document.querySelectorAll(".list[data-list-id]")) {
  list.addEventListener("dragover", (event) => {
    if (!dragged || list.contains(dragged)) return;
    event.preventDefault();
    list.classList.add("drop-target");
  });
  list.addEventListener("dragleave", (event) => {
    if (!list.contains(event.relatedTarget)) list.classList.remove("drop-target");
  });
  list.addEventListener("drop", (event) => {
    event.preventDefault();
    list.classList.remove("drop-target");
    const form = dragged.querySelector("form.move");
    form.querySelector("input").value = list.dataset.listId;
    form.submit();
  });
}

// Picking a file uploads it right away: there is no separate button.
for (const input of document.querySelectorAll("form.attach input[type=file]")) {
  input.addEventListener("change", () => input.form.submit());
}
