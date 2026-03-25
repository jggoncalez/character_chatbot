import { Component } from '@angular/core';
import { ITeamConfig } from './interfaces/team-config';
import { ILinkConfig } from './interfaces/link-config';

@Component({
  selector: 'app-about-us',
  imports: [],
  templateUrl: './about-us.html',
  styleUrl: './about-us.scss',
})
export class AboutUs {
  team : ITeamConfig[] = [
    {
      fullName : "Victor Hugo Camargo",
      role : "Frontend",
      describe : "Desenvolvedor do frontend, utilizando o framework Angular",
      wayImg : "https://placehold.co/100",
      links : {
        github : "https://github.com/VictorHCamargo",
        linkedin : "https://www.linkedin.com/in/victor-hugo-camargo-242926356/"
      }
    },
    {
      fullName : "João Gabriel Gonçalves",
      role : "Backend e Api",
      describe : "Desenvolvedor do backend e responsavel pelo desenvolvimento da Api",
      wayImg : "https://placehold.co/100",
      links : {
        github : "https://github.com/jggoncalez"
      }
    },
    {
      fullName : "Kayque Costa",
      role : "Design",
      describe : "Responsavel pelo desevolvimento dos design do chatbot",
      wayImg : "https://placehold.co/100",
      links : {
        github : "https://github.com/Kayque48"
      }
    },
    {
      fullName : "Gabriel Ferreira",
      role : "Backend e Api",
      describe : "Esteve presente no desenvolvimento do backend e da Api",
      wayImg : "https://placehold.co/100",
      links : {
        github :"https://github.com/escritor2"
      }
    }
  ]

  links : ILinkConfig[] = [
    {
      name : "Repositório Oficial do Projeto",
      describe : "Olhe nosso codigo dentro do GitHub!!",
      way : "https://github.com/jggoncalez/character_chatbot"
    }
  ]
}
