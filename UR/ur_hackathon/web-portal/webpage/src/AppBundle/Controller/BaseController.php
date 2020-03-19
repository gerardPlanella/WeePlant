<?php

namespace AppBundle\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\Controller;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Annotation\Route;

class BaseController extends Controller
{
    /**
     * @Route("/", name="homepage")
     */
    public function indexAction(Request $request)
    {
        return $this->redirect('/dashboard');
    }

    /**
     * @Route("/dashboard", name="dashboard")
     */
    public function dashBoard(Request $request)
    {
        return $this->render('pages/home.html.twig');
    }

    /**
     * @Route("/robot/{robot}", name="robot")
     */
    public function robot($robot = 1)
    {
        return $this->render('pages/robot.html.twig', array('robot' => $robot));
    }

    /**
     * @Route("/map", name="map")
     */
    public function map()
    {
        return $this->render('pages/map.html.twig');
    }

    /**
     * @Route("/workers", name="workers")
     */
    public function workers()
    {
        return $this->render('pages/workers.html.twig');
    }

    /**
     * @Route("/worker/{name}", name="worker")
     */
    public function worker($name)
    {
        if ($name != "") {
            $username = explode(" ", strtolower($name));
            if (sizeof($username) > 1) {
                $username = "$username[0].$username[1]";
            } else {
                $username = strtolower($name);
            }
            return $this->render('pages/worker.html.twig', array('name' => $name, 'username' => $username));
        }
        return $this->redirect('/dashboard');
    }

    /**
     * @Route("/robots", name="robots")
     */
    public function robots()
    {
        return $this->render('pages/robots.html.twig');
    }

    /**
     * @Route("/mailbox", name="mailbox")
     */
    public function mailbox(Request $request)
    {
        return $this->render('pages/mailbox.html.twig');
    }

    /**
     * @Route("/profile", name="profile")
     */
    public function profile(Request $request)
    {
        return $this->render('pages/profile.html.twig');
    }

    /**
     * @Route("/notifications", name="notifications")
     */
    public function notifications(Request $request)
    {
        return $this->render('pages/notifications.html.twig');
    }
}
