const fs = require('fs');
const path = require('path');
const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');

const argv = yargs(hideBin(process.argv))
    .option('componentName', {
        alias: 'c',
        type: 'string',
        description: 'The name of the React component (e.g., MyComponent)',
        required: true,
    })
    .option('targetPath', {
        alias: 'p',
        type: 'string',
        description: 'The path to the directory containing the component file (e.g., src/components/MyComponent)',
        required: true,
    })
    .option('projectRoot', {
        type: 'string',
        description: 'The root directory of the GuardianRoute project.',
        default: path.resolve(__dirname, '..', '..'), // Assumes script is in scripts/scaffolding
    })
    .help()
    .argv;

function scaffoldReactTest(componentName, targetPath, projectRootDir) {
    const fullTargetPath = path.resolve(projectRootDir, targetPath);
    const testFileName = `${componentName}.test.js`; // Or .jsx, .tsx depending on project setup
    const testFilePath = path.join(fullTargetPath, testFileName);

    // Check if the component file itself exists (optional, but good practice)
    // const componentFileNameJs = `${componentName}.js`;
    // const componentFileNameJsx = `${componentName}.jsx`;
    // const componentFilePathJs = path.join(fullTargetPath, componentFileNameJs);
    // const componentFilePathJsx = path.join(fullTargetPath, componentFileNameJsx);

    // if (!fs.existsSync(componentFilePathJs) && !fs.existsSync(componentFilePathJsx)) {
    //     console.warn(`Warning: Component file for '${componentName}' not found in '${fullTargetPath}'. Test file will still be created.`);
    // }

    if (fs.existsSync(testFilePath)) {
        console.info(`Info: Test file '${testFilePath}' already exists.`);
        return;
    }

    const content = `
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom'; // For extended matchers
import ${componentName} from './${componentName}'; // Assuming component is in the same directory

describe('${componentName}', () => {
    test('renders ${componentName} component', () => {
        render(<${componentName} />);
        // Example assertion: Check if some text or element specific to your component is present
        // For example, if your component renders "Hello, World!":
        // expect(screen.getByText(/Hello, World!/i)).toBeInTheDocument();
        
        // Placeholder assertion:
        expect(true).toBe(true); // Replace with actual test assertions
    });

    // Add more test cases as needed
    // test('handles user interaction correctly', () => {
    //     render(<${componentName} />);
    //     // Simulate user events and assert outcomes
    // });
});
`;

    try {
        fs.mkdirSync(fullTargetPath, { recursive: true }); // Ensure directory exists
        fs.writeFileSync(testFilePath, content.trimStart());
        console.log(`Successfully created boilerplate test file: ${testFilePath}`);
        console.log(`Remember to adjust imports and add specific test logic.`);
    } catch (error) {
        console.error(`Error: Could not write to ${testFilePath}. ${error}`);
    }
}

scaffoldReactTest(argv.componentName, argv.targetPath, argv.projectRoot);