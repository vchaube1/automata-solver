const express = require('express');
const bodyParser = require('body-parser');
const { spawn } = require('child_process');
const cors = require('cors');

const app = express();
const port = 5000;

app.use(cors());
app.use(bodyParser.json());

app.post('/api/automaton', (req, res) => {
    console.log('Received request');
    const automaton = req.body;

    // Prepare the data to pass to the Python script
    let inputData = `${automaton.initialState}\n`;
    inputData += `${automaton.finalStates.join(',')}\n`;
    inputData += `${parseFloat(automaton.probabilityThreshold)}\n`;

    automaton.links.forEach(link => {
        inputData += `${link.source},${link.target},${link.action},${parseFloat(link.probability)}\n`;
    });

    // Debugging: Log the input data
    console.log('Input Data:', inputData);

    // Call the Python script with the input data
    const reachability = spawn('python', ['reachability.py']);

    let output = '';
    reachability.stdout.on('data', (data) => {
        output += data.toString();
    });

    reachability.stderr.on('data', (data) => {
        console.error(`Error: ${data}`);
    });

    reachability.on('close', (code) => {
        if (code !== 0) {
            res.status(500).send(`Error executing reachability: exited with code ${code}`);
        } else {
            res.send(output.trim());
        }
    });

    // Write the input data to the Python script's stdin
    reachability.stdin.write(inputData);
    reachability.stdin.end();
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
