// Dynamic participant management for event forms

// Get clusters data from template or define default
let clustersData = [];
if (typeof clusters !== "undefined") {
  clustersData = clusters;
} else {
  // Fetch from DOM if available
  const firstSelect = document.querySelector('select[name="cluster_id[]"]');
  if (firstSelect) {
    clustersData = Array.from(firstSelect.options)
      .filter((opt) => opt.value)
      .map((opt) => ({ id: parseInt(opt.value), name: opt.text }));
  }
}

function addParticipant() {
  const container = document.getElementById("participants-container");
  const participantRow = document.createElement("div");
  participantRow.className = "participant-row";

  // Build cluster options
  let clusterOptions = '<option value="">Select Cluster</option>';
  clustersData.forEach((cluster) => {
    clusterOptions += `<option value="${cluster.id}">${cluster.name}</option>`;
  });

  participantRow.innerHTML = `
        <select name="cluster_id[]" required>
            ${clusterOptions}
        </select>
        <input type="text" name="participant_name[]" placeholder="Participant Name" required>
        <input type="number" name="position[]" placeholder="Position" min="1" required>
        <input type="number" name="points[]" placeholder="Points" min="0" required>
        <button type="button" class="btn btn-sm btn-danger" onclick="removeParticipant(this)">Remove</button>
    `;

  container.appendChild(participantRow);
}

function removeParticipant(button) {
  const container = document.getElementById("participants-container");
  const participantRows = container.querySelectorAll(".participant-row");

  // Prevent removing the last participant
  if (participantRows.length <= 1) {
    alert("At least one participant is required");
    return;
  }

  button.parentElement.remove();
}

// Form validation
document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("event-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      const container = document.getElementById("participants-container");
      const participantRows = container.querySelectorAll(".participant-row");

      if (participantRows.length === 0) {
        e.preventDefault();
        alert("At least one participant is required");
        return false;
      }

      // Validate each participant row
      let isValid = true;
      participantRows.forEach((row, index) => {
        const cluster = row.querySelector('select[name="cluster_id[]"]').value;
        const name = row.querySelector(
          'input[name="participant_name[]"]'
        ).value;
        const position = row.querySelector('input[name="position[]"]').value;
        const points = row.querySelector('input[name="points[]"]').value;

        if (!cluster || !name || !position || !points) {
          isValid = false;
        }

        if (parseInt(position) < 1) {
          isValid = false;
          alert("Position must be at least 1");
        }

        if (parseInt(points) < 0) {
          isValid = false;
          alert("Points must be at least 0");
        }
      });

      if (!isValid) {
        e.preventDefault();
        return false;
      }
    });
  }
});
