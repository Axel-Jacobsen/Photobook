// Function to create the html element below
const createModal = () => {
    const divStr = '<div id="myModal" class="modal">' +
        '<img id="modal-img">' +
        '<div id="caption"></div>' +
        '</div>'

    // This creates an entire html document with the divStr node in the body - we just need the divStr node
    const modalDoc = new DOMParser().parseFromString(divStr, 'text/html')
    const relevantNode = modalDoc.body.firstChild

    // Exit modal with click or with escape key
    relevantNode.onclick = () => {
        removeModal()
    }
    return relevantNode
}

// Remove a html node from its parent
const removeModal = () => {
    const imgModal = document.getElementById("myModal")
    imgModal ? imgModal.parentElement.removeChild(imgModal) : null
}

// Immediately index all the images, place onclick functionality on all images
let img_list = document.getElementsByTagName("img")
for (let i = 0; i < img_list.length; ++i) {
    let el = img_list.item(i)

    el.onclick = () => {
        const imgModal = createModal()
        el.parentElement.appendChild(imgModal)
        document.getElementById('modal-img').src = el.getAttribute("src").replace('_small', '')
        document.getElementById('caption').innerHTML = el.getAttribute("alt")
    }
}

// On Esc key, remove the modal element to return to the original page
document.addEventListener("keydown", event => {
    if (event.key == "Escape") {
        removeModal()
    }
})
