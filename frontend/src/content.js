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
const axios = require('axios');

const styles = (theme) => ({
  paper: {
    maxWidth: 3000,
    margin: 'auto',
    overflow: 'hidden',
  },
  searchBar: {
    borderBottom: '1px solid rgba(0, 0, 0, 0.12)',
  },
  searchInput: {
    fontSize: theme.typography.fontSize,
  },
  block: {
    display: 'block',
  },
  addUser: {
    marginRight: theme.spacing(1),
  },
  contentWrapper: {
    margin: '40px 16px',
  },
  paper2: {
    maxWidth: 300,
    margin: 'auto',
    overflow: 'hidden',
  },
  slide:{
      width : 200
  }
});
const apiURL = "http://localhost:8080";

function Content(props) {
  const { classes } = props;
  let [text, settext] = useState('article을 입력해주세요');
  let [temperature, setTemp] = useState(1.0);
  let [top_p, setTopp] = useState(0.9);
  let [top_k, setTopk] = useState(10);
  const handleChange = (event) => {
      settext(event.target.value);
  }
function _post(Data) {
  const raw = JSON.stringify(Data);

  const requestOptions = {
    method: 'POST',
    headers: {
      'Content-Type' : 'application/json',
      Accpet: 'application/json',
      'Access-Control-Allow_Origin':'*'
      },
    body: raw
  };

  fetch("localhost:8000/api/user", requestOptions)
    .then(response => settext('response'))
    .then(result => settext('result'))
    .catch(error => settext(error));
  }


  function refresh(){
      settext('');
  }
  function tempslide(event, newValue){
        setTemp(newValue);
  }
  function toppslide(event, newValue){
        setTopp(newValue);
  }
  function topkslide(event, newValue){
        setTopk(newValue);
  }
  function handleClick(){
        const Data ={
            textID: "qGenerator",
            content: text,
            temperature: temperature,
            top_p: top_p,
            top_k: top_k
        }
        _post(Data);

  }

  return (<div>
    <Grid container spacing={2}  alignItems="center">
    <Grid item xs = {8}>
    <Paper className={classes.paper}>

      <AppBar className={classes.searchBar} position="static" color="default" elevation={0}>
        <Toolbar>
          <Grid container spacing={2}  alignItems="center">
            {/* <Grid item>
              <SearchIcon className={classes.block} color="inherit" />
            </Grid> */}
            <Grid item xs>
              <TextField
                fullWidth
                multiline
                rows={10}
                placeholder = 'article 입력'
                value = {text}
                onChange = {handleChange}
                InputProps={{
                  disableUnderline: true,
                  className: classes.searchInput,
                }}
              />
            </Grid>
            <Grid item>
              <Button 
              onClick = {handleClick}
              variant="contained" 
              color="primary"
               className={classes.addUser}>
                생성
              </Button>
              <Tooltip title="Refresh">
                <IconButton onClick = {refresh}>
                  <RefreshIcon className={classes.block} color="inherit" />
                </IconButton>
              </Tooltip>
            </Grid>
          </Grid>

        </Toolbar>
      </AppBar>
      
      <div className={classes.contentWrapper}>
        <List>
        <Typography color="textSecondary" align="center">
          No questions generated 
        </Typography>
        <hr></hr>
        <Typography color="textSecondary" align="center">
          No questions generated 
        </Typography>
        <hr></hr>
        <Typography color="textSecondary" align="center">
          No questions generated 
        </Typography>
        </List>
      </div>
    </Paper>
    </Grid>
    <Grid item xs>
    <Paper className={classes.paper2} align ='center'>
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
            onChange = {tempslide}
        />
        <Typography id="temperature" gutterBottom>
            top_p : {top_p}
        </Typography>
        <Slider
            className={classes.slide}
            defaultValue={0.9}
            aria-labelledby="discrete-slider-small-steps"
            step={0.05}
            marks
            min={0.5}
            max={0.9}
            valueLabelDisplay="auto"
            onChange = {toppslide}
        />
        <Typography id="temperature" gutterBottom>
            top_k : {top_k}
        </Typography>
        <Slider
            className={classes.slide}
            defaultValue={10}
            aria-labelledby="discrete-slider-small-steps"
            step={5}
            marks
            min={5}
            max={40}
            valueLabelDisplay="auto"
            onChange = {topkslide}
        />
    </Paper>
    </Grid>
    </Grid>
    </div>
  );
}

Content.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Content);