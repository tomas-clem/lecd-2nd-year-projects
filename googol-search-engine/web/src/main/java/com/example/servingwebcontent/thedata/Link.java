package com.example.servingwebcontent.thedata;

public class Link {

    private String title, url, parag;


    public Link() {}

    public Link(String title, String url, String parag) {
        this.title = title;
        this.url = url;
        this.parag = parag;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getUrl() {
        return url;
    }

    public void setUrl(String url) {
        this.url = url;
    }

    public String getParag() {
        return parag;
    }

    public void setParag(String parag) {
        this.parag = parag;
    }
}
