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
  }
});

const apiURL = "http://localhost:3080";

function Content(props) {
  const { classes } = props;
  let [Text, setText] = useState('기사를 입력해주세요');
  let [temperature, setTemp] = useState(1.0);
  let [top_p, setTopp] = useState(0.9);
  let [top_k, setTopk] = useState(10);
  const handleChange = (event) => {
    setText(event.target.value);
  }

  function _post(Data) {
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

    fetch("http://localhost:8888/api/article-summarization", requestOptions)
      .then(response => response.json())
      .then(json => setText(json['summary']))
      .catch(error => setText(error));
  }

  function refresh(){
    setText('');
  }

  function tempSlide(event, newValue){
    setTemp(newValue);
  }

  function toppSlide(event, newValue){
    setTopp(newValue);
  }

  function topkSlide(event, newValue){
    setTopk(newValue);
  }

  function handleClick(){
    const Data = {
      textID: "QuestionGeneration",
      content: Text,
      model: "korean",
      temperature: temperature,
      top_p: top_p,
      top_k: top_k,
      sentence_length: "10",
      sentence_count: "3"
      }
    _post(Data);
  }

  return (
    <div>
      <Grid container spacing={2}  alignItems="center">
      <Grid item xs={8}>
      <Paper className={classes.paperPrimary}>
      <AppBar className={classes.searchBar} position="static" color="default" elevation={0}>
        <Toolbar>
          <Grid container spacing={2}  alignItems="center">
            <Grid item>
              <SearchIcon className={classes.block} color="inherit" />
            </Grid>
            <Grid item xs>
              <TextField
                fullWidth
                multiline
                rows={10}
                placeholder='기사를 입력해주세요'
                value={Text}
                onChange={handleChange}
                InputProps={{
                  disableUnderline: true,
                  className: classes.searchInput,
                }}
              />
            </Grid>
            <Grid item>
              <Button 
                onClick={handleClick}
                variant="contained"
                color="primary"
                className={classes.button}>
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
    </div>
  );
}

Content.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Content);