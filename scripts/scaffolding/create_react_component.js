#!/usr/bin/env node
/* eslint-disable no-console */

const fs = require('fs-extra');
const path = require('path');
const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');

const argv = yargs(hideBin(process.argv))
  .option('componentName', {
    alias: 'n',
    type: 'string',
    description: 'Name of the component (PascalCase)',
    demandOption: true,
  })
  .option('targetPath', {
    alias: 'p',
    type: 'string',
    description: 'Target path within src (e.g., "features/Settings", "components/Shared")',
    default: 'components', // Default path within 'frontend/src'
  })
  .option('with-css-module', {
    type: 'boolean',
    description: 'Create a .module.css file',
    default: true, // Defaulting to true as it's common
  })
  .option('with-test', {
    type: 'boolean',
    description: 'Create a .test.js file',
    default: true, // Defaulting to true
  })
  .option('with-stories', {
    type: 'boolean',
    description: 'Create a .stories.js file (Storybook)',
    default: false, // Defaulting to false as Storybook might not always be used
  })
  .option('with-error-handler', {
    type: 'boolean',
    description: 'Include boilerplate for useErrorHandler and ErrorDisplay',
    default: false,
  })
  .help()
  .alias('help', 'h')
  .argv;

const { componentName, targetPath } = argv;
const withCssModule = argv['with-css-module'];
const withTest = argv['with-test'];
const withStories = argv['with-stories'];
const withErrorHandler = argv['with-error-handler'];

if (!componentName || !/^[A-Z][A-Za-z0-9]+$/.test(componentName)) {
  console.error('Error: Component name must be in PascalCase (e.g., UserProfile).');
  process.exit(1);
}

const projectRoot = process.cwd(); // Assumes script is run from the new project's root
// Target path is now relative to 'frontend/src'
const componentRootPath = path.join(projectRoot, 'frontend', 'src', targetPath, componentName);


// --- Template Functions ---

const getJsxContent = (name, useCssModule, useErrorHandler) => {
  const errorHandlerImports = useErrorHandler
    ? `import useErrorHandler from 'hooks/useErrorHandler'; // Assuming jsconfig.json for absolute path
import ErrorDisplay from 'components/ErrorDisplay/ErrorDisplay'; // Assuming jsconfig.json
` : '';
  
  const errorHandlerHook = useErrorHandler
    ? `  const { error, errorType, handleError, clearError } = useErrorHandler();\n`
    : '';

  const errorHandlerExample = useErrorHandler
    ? `
  // Example async function
  // const fetchData = async () => {
  //   clearError();
  //   try {
  //     // const result = await someApiService();
  //     // process(result);
  //   } catch (err) {
  //     handleError(err);
  //   }
  // };
` : '';

  const errorDisplayElement = useErrorHandler
    ? `      {error && (
        <ErrorDisplay
          error={error}
          errorType={errorType}
          onClose={clearError}
          // onRetry={fetchData} // Optional: if you have a retry mechanism
        />
      )}\n`
    : '';

  return `import React from 'react';
import PropTypes from 'prop-types';
${useCssModule ? `import styles from './${name}.module.css';\n` : ''}${errorHandlerImports}
/**
 * @param {object} props - The component's props.
 * @returns {JSX.Element} The rendered ${name} component.
 */
const ${name} = (props) => {
  // const { exampleProp } = props;
${errorHandlerHook}
${errorHandlerExample}
  return (
    <div className={${useCssModule ? 'styles.wrapper' : "''"}}>
${errorDisplayElement}      {/* TODO: Implement ${name} content */}
      <p>${name} works!</p>
    </div>
  );
};

${name}.propTypes = {
  // TODO: Define prop types
  // exampleProp: PropTypes.string.isRequired,
};

${name}.defaultProps = {
  // exampleProp: 'default value',
};

export default ${name};
`;
};

const getCssModuleContent = (name) => `/* Styles for ${name} */
.wrapper {
  /* TODO: Add styles for the wrapper div */
  padding: 1rem;
  border: 1px solid #ccc;
}
`;

const getTestContent = (name) => `import React from 'react';
import { render, screen } from '@testing-library/react';
import ${name} from './${name}';

describe('${name}', () => {
  test('renders correctly', () => {
    render(<${name} />);
    // Example assertion:
    expect(screen.getByText('${name} works!')).toBeInTheDocument();
  });

  // TODO: Add more tests for props, interactions, etc.
});
`;

const getStoriesContent = (name, storybookPath) => `import React from 'react';
import ${name} from './${name}';

export default {
  title: '${storybookPath}/${name}',
  component: ${name},
  // argTypes: {
  //   exampleProp: { control: 'text' },
  // },
};

const Template = (args) => <${name} {...args} />;

export const Default = Template.bind({});
Default.args = {
  // exampleProp: 'Hello World',
};

// TODO: Add more stories for different states/props
`;


// --- Main Script Logic ---

async function scaffoldComponent() {
  try {
    if (await fs.pathExists(componentRootPath)) {
      console.error(`Error: Component directory already exists at ${componentRootPath}`);
      process.exit(1);
    }
    await fs.ensureDir(componentRootPath);
    console.log(`Created directory: ${componentRootPath}`);

    // Create JSX file
    const jsxFilePath = path.join(componentRootPath, `${componentName}.jsx`);
    await fs.writeFile(jsxFilePath, getJsxContent(componentName, withCssModule, withErrorHandler));
    console.log(`Created file: ${jsxFilePath}`);

    // Create CSS Module file
    if (withCssModule) {
      const cssFilePath = path.join(componentRootPath, `${componentName}.module.css`);
      await fs.writeFile(cssFilePath, getCssModuleContent(componentName));
      console.log(`Created file: ${cssFilePath}`);
    }

    // Create Test file
    if (withTest) {
      const testFilePath = path.join(componentRootPath, `${componentName}.test.js`);
      await fs.writeFile(testFilePath, getTestContent(componentName));
      console.log(`Created file: ${testFilePath}`);
    }

    // Create Stories file
    if (withStories) {
      const storiesFilePath = path.join(componentRootPath, `${componentName}.stories.js`);
      // Construct a sensible Storybook title path
      const storybookTitlePath = targetPath.startsWith('src/') ? targetPath.substring(4) : targetPath;
      await fs.writeFile(storiesFilePath, getStoriesContent(componentName, storybookTitlePath));
      console.log(`Created file: ${storiesFilePath}`);
    }

    console.log(`\nSuccessfully scaffolded ${componentName} component in ${componentRootPath}`);
    console.log("Remember to update imports and use the new component where needed.");

  } catch (error) {
    console.error('Failed to scaffold component:', error);
    process.exit(1);
  }
}

scaffoldComponent();