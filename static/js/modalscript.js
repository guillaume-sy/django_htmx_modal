let removeFadeOut=( el, speed )=> {
    const seconds = speed/1000;
    el.style.transition = "opacity "+seconds+"s ease";

    el.style.opacity = 0;
    setTimeout(function() {
        el.parentNode.removeChild(el);
    }, speed);
}

let setFactoryValue = (id) => {
    let selectedFactory= document.getElementById(`factory-button-${id}`)
    let parentDiv = selectedFactory.parentNode.parentNode;
    let selectedFactoryNameValue = parentDiv.firstElementChild.innerHTML
    let factoryValueToSet= document.getElementById(`hidden_factory_value`)
    factoryValueToSet.value= selectedFactory.value
    let factoryNameToShow= document.getElementById(`form__visible__factory_name_display`)
     factoryNameToShow.innerHTML= selectedFactoryNameValue
    let modalDisplayed= document.getElementById(`factory-modal`)
    if(modalDisplayed){
        removeFadeOut(modalDisplayed, 200);
    }
};

