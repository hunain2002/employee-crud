document.addEventListener("DOMContentLoaded", () => {
  const video = document.getElementById('camera');

  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        video.srcObject = stream;
        video.play();
      })
      .catch(err => {
        console.error("Camera access denied or not supported:", err);
        alert("Unable to access camera. Please check permissions.");
      });
  } else {
    alert("Your browser does not support accessing the webcam.");
  }
});

function captureAttendance() {
  const canvas = document.getElementById('snapshot');
  const ctx = canvas.getContext('2d');
  const video = document.getElementById('camera');
  const empId = document.getElementById('employee_id').value;

  if (!empId) {
    alert("Employee ID is required.");
    return;
  }

  canvas.width = 320;
  canvas.height = 240;
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

  const photoData = canvas.toDataURL("image/png");

  fetch('/mark_attendance_photo', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      employee_id: empId,
      photo: photoData
    })
  })
    .then(response => {
      if (!response.ok) {
        throw new Error("Server error");
      }
      return response.text();
    })
    .then(msg => alert(msg))
    .catch(err => {
      console.error("Attendance error:", err);
      alert("Failed to mark attendance. Try again.");
    });
}
