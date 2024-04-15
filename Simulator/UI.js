{\rtf1\ansi\ansicpg1252\cocoartf2708
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 document.addEventListener("DOMContentLoaded", function() \{\
  const validUserIDs = [\
    "5829743", "1038456", "7290518", "3468970", "6152038",\
    "8974062", "4201853", "1789352", "6321094", "9548021"\
  ];\
\
  const validPasswords = [\
    "P@ssw0r", "Secur1T", "3xample", "Passw0$", "rAnD0m1",\
    "Ch@nge!", "7esting", "P@55w0r", "F1r3w4l", "s3cur3!"\
  ];\
\
  const loginButton = document.querySelector(".login");\
  const guestButton = document.querySelector(".guest");\
  const userIDInput = document.querySelector("input[type='text']");\
  const passwordInput = document.querySelector("input[type='password']");\
\
  loginButton.addEventListener("click", function() \{\
    const enteredUserID = userIDInput.value.trim();\
    const enteredPassword = passwordInput.value.trim();\
\
    if (validUserIDs.includes(enteredUserID) && validPasswords.includes(enteredPassword)) \{\
      window.location.href = "https://example.com";\
    \} else \{\
      alert("Invalid username or password. Please try again.");\
    \}\
  \});\
\
  guestButton.addEventListener("click", function() \{\
    \
    window.location.href = "https://codepen.io/Casandra-Walker/pen/mdgqKOz";\
  \});\
\});\
}