import React, {useState} from 'react';
import PropTypes from 'prop-types';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import TextField from '@material-ui/core/TextField';
import Tooltip from '@material-ui/core/Tooltip';
import IconButton from '@material-ui/core/IconButton';
import { withStyles } from '@material-ui/core/styles';
import SearchIcon from '@material-ui/icons/Search';
import RefreshIcon from '@material-ui/icons/Refresh';
import Slider from '@material-ui/core/Slider';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import InputLabel from '@material-ui/core/InputLabel';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import NativeSelect from '@material-ui/core/NativeSelect';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import ListSubheader from '@material-ui/core/ListSubheader';
import clsx from 'clsx';
import Backdrop from '@material-ui/core/Backdrop';
import CircularProgress from '@material-ui/core/CircularProgress';
import fetchIntercept from 'fetch-intercept';

const styles = (theme) => ({
  paperPrimary: {
    maxWidth: 3000,
    margin: 'auto',
    overflow: 'hidden',
  },
  paperSecondary: {
    maxWidth: 300,
    margin: 'auto',
    overflow: 'hidden',
  },
  generateBar: {
    borderBottom: '1px solid rgba(0, 0, 0, 0.12)',
  },
  generateInput: {
    fontSize: theme.typography.fontSize,
  },
  block: {
    display: 'block',
  },
  button: {
    marginRight: theme.spacing(1),
  },
  contentWrapper: {
    margin: '40px 16px',
  },
  slide:{
    width : 200
  },
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  me:{
    textAlign: 'right'
  },
  bot:{
    textAlign : 'left'
  },
  backdrop: {
    zIndex: theme.zIndex.drawer + 1,
    color: '#fff',
  },
});

const apiURL = "http://localhost:8888";

function Chat_bot(props) {
  const { classes } = props;
  let [model, setModel] = useState('korquad');
  let [result, setResult] = useState('');
  let [Text, setText] = useState('');
  let [converse, setConverse] = useState([]);
  let [temperature, setTemp] = useState(1.0);
  let [top_p, setTopp] = useState(0.9);
  let [top_k, setTopk] = useState(10);
  let [state, setState] = useState(false);
  const unregister = fetchIntercept.register({
    request: function (url, config) {
        setState(true);
        return [url, config];
    },

    requestError: function (error) {
      setState(false);
        return Promise.reject(error);
    },

    response: function (response) {
      setState(false);
        return response;
    },

    responseError: function (error) {
      setState(false);
        return Promise.reject(error);
    }
});
  function _post(text) {
    unregister();
    const Data = {
      textID: "Chat-Bot",
      content: text,
      model: model,
      temperature: temperature,
      top_p: top_p,
      top_k: top_k,
      sentence_length: "10",
      sentence_count: "3"
    }
    const raw = JSON.stringify(Data);

    const requestOptions = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': '*',
      },
      body: raw
    };

    fetch(`${apiURL}/api/question-generation`, requestOptions)
      .then(response => response.json())
      .then(json=>setResult(json['sentence']))
      .catch(error => setText(error));
  };

  function refresh(){
    setText('');
    setConverse([]);
  };
  
  const handleChange = (event) => {
    setText(event.target.value);
  };

  function addChat(text){
    var temp = [...converse, {id : text, toggle : 0}];
    setConverse(temp);
    setText('');
    _post(text);
    temp = [...temp, {id : result, toggle : 1}];
    setConverse(temp);
  };

  function handleClick(){
    addChat(Text);
  };

  function tempSlide(event, newValue){
    setTemp(newValue);
  };

  function toppSlide(event, newValue){
    setTopp(newValue);
  };

  function topkSlide(event, newValue){
    setTopk(newValue);
  };

  const handleModel = (event) => {
    setModel(event.target.value);
  };

  const keyHandler = (event)=>{
    if(event.key === "Enter"){
      addChat(Text);
    }
  };
  return (
    <div>
      <Toolbar>
        <FormControl className={classes.formControl}>
          <InputLabel shrink htmlFor="model selection">
           모델
          </InputLabel>
          <NativeSelect
            onChange={handleModel}
            inputProps={{
            name: 'models',
            id: 'model selection',
            }}
          >
            <option value="chatbot">챗봇모델</option>
          </NativeSelect>
        {/* <FormHelperText>Label + placeholder</FormHelperText> */}
        </FormControl>
        <FormControl className={classes.formControl}>
          <InputLabel shrink htmlFor="example selection">
          예시
          </InputLabel>
          <NativeSelect
          
            inputProps={{
              name: 'examples',
              id: 'example selection',
            }}
          >
          <option value="">None</option>
         </NativeSelect>
        {/* <FormHelperText>Label + placeholder</FormHelperText> */}
        </FormControl>
      </Toolbar>

      <Grid container spacing={2}  alignItems="center">
        <Grid item xs={8}>
          <Paper className={classes.paperPrimary}>
            <div className={classes.contentWrapper}>
              <List style={{height: '500px', border:'1px solid black', overflow: 'hidden'}}>
                <ListSubheader/>
              {converse.map(({ id: childId, toggle: user }) => (
              <ListItem
                value = {user}
                key={childId}
              >
              <ListItemText
                className={clsx((!user)&&classes.me, (user)&&classes.bot)}
              >
                {childId}
              </ListItemText>
              </ListItem>
            ))}
              </List>
            </div>
              <Divider variant="middle" />
            
              <Toolbar>
                <Grid container spacing={2}  alignItems="center">
                  <Grid item xs>
                    <TextField
                      fullWidth
                      placeholder='대화를 입력해주세요'
                      value={Text}
                      onKeyDown={keyHandler}
                      onChange={handleChange}
                      InputProps={{
                        disableUnderline: true,
                        className: classes.searchInput,
                      }}
                    />
                  </Grid>

                  <Grid item>
                    <Button onClick={handleClick} variant="contained" color="primary" className={classes.button}>
                      생성
                    </Button>
                    <Tooltip title="Refresh">
                      <IconButton onClick={refresh}>
                        <RefreshIcon className={classes.block} color="inherit" />
                      </IconButton>
                    </Tooltip>
                  </Grid>
                </Grid>
              </Toolbar>
            </Paper>
          </Grid>
        <Grid item xs>
          <Paper className={classes.paperSecondary} align ='center'>
            <Typography id="temperature" gutterBottom>
              temperature : {temperature}
            </Typography>
            <Slider
              className={classes.slide}
              defaultValue={1.0}
              aria-labelledby="discrete-slider-small-steps"
              step={0.1}
              marks
              min={0.5}
              max={2.0}
              valueLabelDisplay="auto"
              onChange = {tempSlide}
            />
            <Typography id="top_p" gutterBottom>
              top_p : {top_p}
            </Typography>
            <Slider
              className={classes.slide}
              defaultValue={0.9}
              aria-labelledby="discrete-slider-small-steps"
              step={0.05}
              marks
              min={0.5}
              max={1.0}
              valueLabelDisplay="auto"
              onChange = {toppSlide}
            />
            <Typography id="top_k" gutterBottom>
              top_k : {top_k}
            </Typography>
            <Slider
              className={classes.slide}
              defaultValue={10}
              aria-labelledby="discrete-slider-small-steps"
              step={5}
              marks
              min={5}
              max={100}
              valueLabelDisplay="auto"
              onChange = {topkSlide}
            />
          </Paper>
        </Grid>
      </Grid>
      <Backdrop className={classes.backdrop} open={state}>
        <CircularProgress color="inherit" />
      </Backdrop>
    </div>
  );
}

Chat_bot.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Chat_bot);