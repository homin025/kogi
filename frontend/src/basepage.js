import React from 'react';
import PropTypes from 'prop-types';
import {createMuiTheme, ThemeProvider, withStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Hidden from '@material-ui/core/Hidden';
import Question_generation from './question_generation';
import Tale_generation from './tale_generation';
import Review_generation from './review_generation';
import Article_summarization from './article_summarization';
import Chat_bot from './chat_bot'
import Header from './header';
import clsx from 'clsx';
import Divider from '@material-ui/core/Divider';
import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import kogi from './kogi.jpg';

import ContactSupportSharpIcon from '@material-ui/icons/ContactSupportSharp';
import QuestionAnswerSharpIcon from '@material-ui/icons/QuestionAnswerSharp';
import AssignmentSharpIcon from '@material-ui/icons/AssignmentSharp';
import MenuBookSharpIcon from '@material-ui/icons/MenuBookSharp';
import EditLocationSharpIcon from '@material-ui/icons/EditLocationSharp';
let theme = createMuiTheme({
  palette: {
    primary: {
      light: '#63ccff',
      main: '#009be5',
      dark: '#006db3',
    },
  },
  typography: {
    h5: {
      fontWeight: 500,
      fontSize: 26,
      letterSpacing: 0.5,
    },
  },
  shape: {
    borderRadius: 8,
  },
  props: {
    MuiTab: {
      disableRipple: true,
    },
  },
  mixins: {
    toolbar: {
      minHeight: 48,
    },
  },
});

theme = {
  ...theme,
  overrides: {
    MuiDrawer: {
      paper: {
        backgroundColor: '#18202c',
      },
    },
    MuiButton: {
      label: {
        textTransform: 'none',
      },
      contained: {
        boxShadow: 'none',
        '&:active': {
          boxShadow: 'none',
        },
      },
    },
    MuiTabs: {
      root: {
        marginLeft: theme.spacing(1),
      },
      indicator: {
        height: 3,
        borderTopLeftRadius: 3,
        borderTopRightRadius: 3,
        backgroundColor: theme.palette.common.white,
      },
    },
    MuiTab: {
      root: {
        textTransform: 'none',
        margin: '0 16px',
        minWidth: 0,
        padding: 0,
        [theme.breakpoints.up('md')]: {
          padding: 0,
          minWidth: 0,
        },
      },
    },
    MuiIconButton: {
      root: {
        padding: theme.spacing(1),
      },
    },
    MuiTooltip: {
      tooltip: {
        borderRadius: 4,
      },
    },
    MuiDivider: {
      root: {
        backgroundColor: '#404854',
      },
    },
    MuiListItemText: {
      primary: {
        fontWeight: theme.typography.fontWeightMedium,
      },
    },
    MuiListItemIcon: {
      root: {
        color: 'inherit',
        marginRight: 0,
        '& svg': {
          fontSize: 20,
        },
      },
    },
    MuiAvatar: {
      root: {
        width: 32,
        height: 32,
      },
    },
  },
};

const drawerWidth = 170;

const styles = {
  root: {
    display: 'flex',
    minHeight: '100vh',
  },
  drawer: {
    [theme.breakpoints.up('sm')]: {
      width: drawerWidth,
      flexShrink: 0,
    },
  },
  app: {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
  },
  main: {
    flex: 1,
    padding: theme.spacing(4, 6),
    background: '#eaeff1',
  },
  footer: {
    padding: theme.spacing(2),
    background: '#eaeff1',
  },
  firebase: {
    fontSize: 24,
    color: theme.palette.common.white,
  },
  categoryHeader: {
    paddingTop: theme.spacing(2),
    paddingBottom: theme.spacing(2),
  },
  categoryHeaderPrimary: {
    color: theme.palette.common.white,
  },
  item: {
    paddingTop: 1,
    paddingBottom: 1,
    color: 'rgba(255, 255, 255, 0.7)',
    '&:hover,&:focus': {
      backgroundColor: 'rgba(255, 255, 255, 0.08)',
    },
  },
  itemCategory: {
    backgroundColor: '#232f3e',
    boxShadow: '0 -1px 0 #404854 inset',
    paddingTop: theme.spacing(2),
    paddingBottom: theme.spacing(2),
  },
  itemActiveItem: {
    color: '#4fc3f7',
  },
  itemPrimary: {
    fontSize: 'inherit',
  },
  itemIcon: {
    minWidth: 'auto',
    marginRight: theme.spacing(2),
  },
  divider: {
    marginTop: theme.spacing(2),
  },
};

function Paperbase(props) {
  let [button, setButton] = React.useState([true, false, false, false, false]);
  const {...other } = props;
  const categories = [
    {
      id: '기능',
      children: [
        { id: '질문생성', icon: <ContactSupportSharpIcon/>, active: button[0], bvalue : 0},
        { id: '기사요약', icon: <AssignmentSharpIcon/> , active: button[1], bvalue : 1},
        { id: '동화창작', icon: <MenuBookSharpIcon/>, active: button[2], bvalue : 2 },
        { id: '리뷰생성', icon: <EditLocationSharpIcon/> , active: button[3], bvalue : 3},
        { id: '챗봇모델', icon: <QuestionAnswerSharpIcon /> , active: button[4], bvalue : 4},
      ],
    },
  ];
  
  const { classes } = props;
  const [mobileOpen, setMobileOpen] = React.useState(false);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleListItemClick = (event, index) => {
    setContent(index);
    var buttons =[false, false, false, false, false];
    buttons[index] = true;
    setButton(buttons);
  };

  const [content, setContent] = React.useState(0);
  function Content() {
    if(content === 0) return <Question_generation/>;
    else if(content === 1){return <Article_summarization/>}
    else if(content === 2){return <Tale_generation/>}
    else if(content === 3){return <Review_generation/>}
    else if(content === 4){return <Chat_bot/>}
  }
  
  return (
    <ThemeProvider theme={theme}>
      <div className={classes.root}>
        <CssBaseline />
        {/* <Grid container spacing={2}  alignItems="center">
        <Grid item xs={2}> */}
        <nav className={classes.drawer}>
          <Hidden xsDown implementation="css">
            <Drawer variant="permanent" {...other}>
              <List disablePadding>
                <ListItem className={clsx(classes.firebase, classes.item, classes.itemCategory)}>
                  <img src = {kogi} width='150' alt=''/>
                </ListItem>
                {categories.map(({ id, children }) => (
                  <React.Fragment key={id}>
                    <ListItem className={classes.categoryHeader}>
                      <ListItemText
                        classes={{
                          primary: classes.categoryHeaderPrimary,
                        }}>
                        {id}
                      </ListItemText>
                    </ListItem>
                    {children.map(({ id: childId, icon, active, bvalue }) => (
                      <ListItem
                        key={childId}
                        value={bvalue}
                        button
                        onClick={(event) => handleListItemClick(event, bvalue)}
                        className={clsx(classes.item, active && classes.itemActiveItem)}
                      >
                        <ListItemIcon className={classes.itemIcon}>{icon}</ListItemIcon>
                        <ListItemText
                          classes={{
                            primary: classes.itemPrimary,
                          }}>
                          {childId}
                        </ListItemText>
                      </ListItem>
                    ))}
                    <Divider className={classes.divider} />
                  </React.Fragment>
                ))}
              </List>
            </Drawer>
          </Hidden>
        </nav>
        
        <div className={classes.app}>
          <Header index = {content} onDrawerToggle={handleDrawerToggle} />
          <main className={classes.main}>
            {Content()}
          </main>
          <footer className={classes.footer}>
          </footer>
        </div>
      </div>
    </ThemeProvider>
  );
}

Paperbase.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Paperbase);