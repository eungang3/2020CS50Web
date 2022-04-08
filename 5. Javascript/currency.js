document.addEventListener('DOMContentLoaded', function(){

    document.querySelector('form').onsubmit = () => {

        API_KEY = '284b4a65480cae5859ffd12234443577';
        fetch('http://api.exchangeratesapi.io/v1/latest?access_key=' + API_KEY)
        .then(response => response.json())
        .then(data => {
            const currency = document.querySelector('#currency').value.toUpperCase();
            const rate = data.rates[currency];
            if (rate !== undefined){
                document.querySelector('#result').innerHTML = `1 EUR is ${rate}.`
            } else {
                document.querySelector('#result').innerHTML = `Invalid currency.`
            }
        })
        .catch(error => {
            console.log('error: ', error);
        })
        return false;
    }

})