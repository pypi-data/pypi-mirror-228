import { useState, useEffect } from 'react';
import { ThemeProvider, BaseStyles, Box, UnderlineNav } from '@primer/react';
import { CpuIcon, CodeIcon, AlertIcon, HistoryIcon, CommentDiscussionIcon } from '@primer/octicons-react';
import Tab1 from './tabs/Tab1';
import Tab2 from './tabs/Tab2';
import Tab3 from './tabs/Tab3';
import Tab4 from './tabs/Tab4';
import Tab5 from './tabs/Tab5';
import { requestAPI } from './handler';

const Tabs = (): JSX.Element => {
  const [tab, setTab] = useState(1);
  const [version, setVersion] = useState('');
  useEffect(() => {
    requestAPI<any>('config')
    .then(data => {
      setVersion(data.version);
    })
    .catch(reason => {
      console.error(
        `Error while accessing the jupyter server jupyter_functions extension.\n${reason}`
      );
    });
  }, []);
  return (
    <>
      <ThemeProvider>
        <BaseStyles>
          <Box style={{maxWidth: 700}}>
            <Box>
              <UnderlineNav aria-label="jupyter-functions">
                <UnderlineNav.Item aria-current={tab === 1 ? "page" : undefined} aria-label="tab-1" icon={CpuIcon} onSelect={e => {e.preventDefault(); setTab(1);}}>
                  Kernels
                </UnderlineNav.Item>
                <UnderlineNav.Item aria-current={tab === 2 ? "page" : undefined} icon={CodeIcon} counter={6} aria-label="tab-2" onSelect={e => {e.preventDefault(); setTab(2);}}>
                  Notebooks
                </UnderlineNav.Item>
                <UnderlineNav.Item aria-current={tab === 3 ? "page" : undefined} icon={AlertIcon} aria-label="tab-3" onSelect={e => {e.preventDefault(); setTab(3);}}>
                  Warnings
                </UnderlineNav.Item>
                <UnderlineNav.Item aria-current={tab === 4 ? "page" : undefined} icon={HistoryIcon} counter={7} aria-label="tab-4" onSelect={e => {e.preventDefault(); setTab(4);}}>
                  History
                </UnderlineNav.Item>
                <UnderlineNav.Item aria-current={tab === 5 ? "page" : undefined} icon={CommentDiscussionIcon} aria-label="tab-5" onSelect={e => {e.preventDefault(); setTab(5);}}>
                  More
                </UnderlineNav.Item>
              </UnderlineNav>
            </Box>
            <Box m={3}>
              {(tab === 1) && <Tab1 version={version}/>}
              {(tab === 2) && <Tab2/>}
              {(tab === 3) && <Tab3/>}
              {(tab === 4) && <Tab4/>}
              {(tab === 5) && <Tab5/>}
            </Box>
          </Box>
        </BaseStyles>
      </ThemeProvider>
    </>
  );
}

export default Tabs;
