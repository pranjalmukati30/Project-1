//document.getElementById("userForm").addEventListener("submit", async function (event) {
//    event.preventDefault(); // stop page reload
//
//    const userData = {
//        name: document.getElementById("name").value,
//        email: document.getElementById("email").value,
//        gender: document.getElementById("gender").value,
//        age: parseInt(document.getElementById("age").value),
//        city: document.getElementById("city").value
//    };
//
//    try {
//        const response = await fetch("/create_users", {
//            method: "POST",
//            headers: {
//                "Content-Type": "application/json"
//            },
//            body: JSON.stringify(userData)
//        });
//
//        const result = await response.json();
//
//        document.getElementById("responseMessage").innerText = result.message || result.error;
//
//        document.getElementById("userForm").reset();
//
//    } catch (error) {
//        document.getElementById("responseMessage").innerText = "Something went wrong!";
//    }
//});